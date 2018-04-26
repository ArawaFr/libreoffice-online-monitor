#!/usr/bin/env python

import asyncio
import websockets
import logging
import functools
import os
import signal

logger = logging.getLogger('loolmonitor')


def debug_websocket(websocket):
    logger.debug ("| -- Web Socket Message -- |")
    logger.debug ("| request_headers: {}".format(websocket.request_headers))
    logger.debug ("| response_headers: {}".format(websocket.response_headers))
    logger.debug ("| local_address: {}".format(websocket.local_address))
    logger.debug ("| remote_address: {}".format(websocket.remote_address))
    logger.debug ("| ------------------------ |")

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
        debug_websocket(websocket)
        logger.debug ("Path: {}".format(path))

    async def run(self):
        """
        Infite loop that call handle_message for each received message.
        Prevent deconnection by sedding ping query every 20s
        """
        while self.alive:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=20)
                debug_websocket(self.websocket)
            except websockets.exceptions.ConnectionClosed:
                self.close()
            except asyncio.TimeoutError:
                # No data in 20 seconds, check the connection.
                await self.pong_waiter()
            else:
                self.handle_message(message)
                await self.websocket.send(message)

    def close(self):
        logger.info ("Connection {} closed by client".format(self.websocket.remote_address))
        debug_websocket(self.websocket)
        self.alive = False

    def handle_message(self, message):
        """
        You want to override this method.
        self.alive=False to end current session
        """
        print(message)

    async def pong_waiter(self):
        """Send ping query. Close session if Timeout"""
        try:
            pong_waiter = await self.websocket.ping()
            await asyncio.wait_for(pong_waiter, timeout=10)
        except asyncio.TimeoutError:
            # No response to ping in 10 seconds, disconnect.
            self.alive = False

class LoolMonitor():
    """
    Create websocket server
    Catch SIGINT and SIGTERM to stop the server
    """
    def __init__(self, host='127.0.0.1', port=8765):
        self.__loop = None
        self.__host = host
        self.__port = port

    async def handler(self, websocket, path):
        handler = GenericHandler(websocket, path)
        await handler.run()

    def ask_exit(self, signame):
        logger.info ("got signal %s: exit" % signame)
        self.__loop.stop()

    def __init_event_loop(self):
        self.__loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            self.__loop.add_signal_handler(getattr(signal, signame),
                                    functools.partial(self.ask_exit, signame))

    def start(self):
        start_server = websockets.serve(self.handler, self.__host, self.__port)

        logger.info ("listing on 'ws://{}:{}'".format(self.__host, self.__port))
        logger.info ("Event loop running forever, press Ctrl+C to interrupt.")
        logger.info ("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())

        try:
            self.__init_event_loop()
            self.__loop.run_until_complete(start_server)
            self.__loop.run_forever()
        finally:
            self.__loop.close()
