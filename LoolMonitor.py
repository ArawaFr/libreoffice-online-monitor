#!/usr/bin/env python

import asyncio, functools
import websockets, socket
import logging
import os, signal

logger = logging.getLogger(__name__)


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
