#!/usr/bin/env python

import asyncio, functools
import websockets, socket
import logging
import os, signal

logger = logging.getLogger(__name__)

class GenericHandler():
    """
    Instanciate for each websocket session.
    You probably want to override handle_message function.
    """

    def __init__(self, websocket, path):
        self.websocket = websocket
        self.path = path
        self.alive = True

        logger.info ("New Worker {} Connected".format(websocket.remote_address))
        logger.debug ("$ Path: {}".format(path))

    async def wsSend(self, msg):
        logger.info ("Send Message {}".format(msg))
        await self.websocket.send(msg)

    async def run(self):
        """
        Infite loop that call handle_message for each received message.
        Prevent deconnection by sedding ping query every 20s
        """
        await self.wsSend("documents")

        while self.alive:
            try:
                logger.debug ("$ waiting for message")
                message = await asyncio.wait_for(self.websocket.recv(), timeout=20)

                logger.debug ("$ handle message")
                rsp = self.handle_message(message)
                if rsp:
                    await self.wsSend(rsp)

            except websockets.exceptions.ConnectionClosed:
                logger.debug ("$ exceptions.ConnectionClosed : close")
                self.close()
            except asyncio.TimeoutError:
                # No data in 20 seconds, check the connection.
                logger.debug ("$ asyncio.TimeoutError : ping pong")
                await self.pong_waiter()
            else:
                logger.debug ("$ else angel")


    def close(self):
        logger.info ("Connection {} closed by client".format(self.websocket.remote_address))
        self.alive = False

    def handle_message(self, message):
        """
        You want to override this method.
        self.alive=False to end current session
        """
        logger.info ("Handle Message {}".format(message))
        print(message)
        return message

    async def pong_waiter(self):
        """Send ping query. Close session if Timeout"""
        try:
            pong_waiter = await self.websocket.ping()
            await asyncio.wait_for(pong_waiter, timeout=10)
        except asyncio.TimeoutError:
            # No response to ping in 10 seconds, disconnect.
            self.alive = False

class LoolAdminHandler(GenericHandler):
    """
    Handler that subscribe and get stats from lool
    """
    def handle_message(self, message):
        """
        You want to override this method.
        self.alive=False to end current session
        """
        logger.info ("ADM: Handle Message {}".format(message))
        print(message)
        return "documents"

class LoolMonitor():
    """
    Create websocket server
    Catch SIGINT and SIGTERM to stop the server
    """
    def __init__(self, host=None, port=8765):
        self.__loop = None
        self.__host = host
        self.__port = port
        self.connected = set()


    async def consumer_handler(self, websocket, path):
        while True:
            logger.debug ("$ waiting for message")
            message = await websocket.recv()
            await self.consumer(message)

    async def consumer(self, message):
        logger.info (":: Handle Message {}".format(message))

    async def producer_handler(self, websocket, path):
        while True:
            message = await self.producer()
            logger.info (":: Send Message {} -- {}".format(message, type(message)))
            await asyncio.wait([ws.send(message) for ws in self.connected])

    async def producer(self):
        logger.debug ("$ waiting for produce")
        await asyncio.sleep(10)
        logger.debug ("$ waiting for produce ... send mem_stats")
        return str("total_avail_mem")

    async def handler(self, websocket, path):
        #handler = LoolAdminHandler(websocket, path)
        #await handler.run()
        self.connected.add(websocket)
        try:
            consumer_task = asyncio.ensure_future(self.consumer_handler(websocket, path))
            producer_task = asyncio.ensure_future(self.producer_handler(websocket, path))
            done, pending = await asyncio.wait([consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED, )

            for task in pending:
                task.cancel()

        finally:
            self.connected.remove(websocket)

    def ask_exit(self, signame):
        logger.info ("got signal %s: exit" % signame)
        self.__loop.stop()

    def __init_event_loop(self):
        self.__loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            self.__loop.add_signal_handler(getattr(signal, signame),
                                    functools.partial(self.ask_exit, signame))

    def start(self):
        start_server = websockets.serve(self.handler, self.__host, self.__port,
                        family=socket.AF_INET, ssl=None)

        logger.info ("listing on 'ws://{}:{}'".format(self.__host, self.__port))
        logger.info ("Event loop running forever, press Ctrl+C to interrupt.")
        logger.info ("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())

        try:
            self.__init_event_loop()
            self.__loop.run_until_complete(start_server)
            self.__loop.run_forever()
        finally:
            self.__loop.close()
