#!/usr/bin/env python
import logging
from multiprocessing import Process, Queue
import queue

logger = logging.getLogger(__name__)

tasks = Queue()

class CmisHandler(Process):
    """
    Handler that call CMIS Server
    """

    def __init__(self):
        super(CmisHandler, self).__init__()
        self.NAME = "CmisHandler"

    def adddoc(self, docKey):
        tasks.put(AddDocTask(docKey))

    def rmdoc(self, docKey):
        tasks.put(RmDocTask(docKey))

    def run(self):
        while True:
            task = tasks.get()
            if task is None:
                break
            task.do_work()

    def stop(self):
        tasks.put(None)


class AddDocTask():
    def __init__(self, docKey=None):
        self.__docKey = docKey

    def do_work(self):
        logger.info ("+++CmisHandler+++ ADD DOC {}".format(self.__docKey))

class RmDocTask():
    def __init__(self, docKey=None):
        self.__docKey = docKey

    def do_work(self):
        logger.info ("+++CmisHandler+++ RM  DOC {}".format(self.__docKey))
