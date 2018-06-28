#!/usr/bin/env python

import asyncio, functools
import websockets, socket
import logging
import os, signal
import json

logger = logging.getLogger(__name__)

STATS_CMD = [
             "active_users_count",
             "active_docs_count",
             "mem_stats",
             "cpu_stats",
             "sent_activity",
             "mem_consumed",
             "total_avail_mem",
             "sent_bytes",
             "recv_bytes",
            ]

# Query Stats every 10s
DOCS_EVERY = 10

class LoolMonitor():
    """
    Create websocket server
    Catch SIGINT and SIGTERM to stop the server
    """

    docs = {}

    def __init__(self, host=None, port=8765):
        self.__loop = None
        self.__host = host
        self.__port = port
        self.connected = set()

    async def consumer_handler(self, websocket, path):
        while True:
            message = await websocket.recv()
            logger.debug (":: Handle Message {} - ws={}".format(message, websocket.remote_address))
            await self.consumer(websocket.remote_address, message)

    async def consumer(self, remote_address, message):
        msg = message.partition(" ")
        cmd = msg[0]
        if cmd in STATS_CMD:
            k = "%s:%d/%s" % sum((remote_address, (cmd,)), ())
            self.stats[k] = msg[2]

        elif cmd == "documents":
            data = json.loads(msg[2])
            docs = data["documents"]
        elif cmd == "loolserver":
            data = json.loads(msg[2])
            logger.info (":: Lool Server Version :: {}".format(data))

        elif cmd == "lokitversion":
            data = json.loads(msg[2])
            logger.info (":: Lokit Version :: {}".format(data))

        else:
            logger.info (":: Unknow Message :: {}".format(cmd))


    async def producer_handler(self, websocket, path):
        await asyncio.wait([ws.send("version") for ws in self.connected])
        while True:
            await asyncio.wait([ws.send("documents") for ws in self.connected])
            await asyncio.sleep(DOCS_EVERY)


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
