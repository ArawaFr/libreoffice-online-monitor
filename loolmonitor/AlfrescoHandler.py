#!/usr/bin/env python
import os
import logging
import re
import requests

from multiprocessing import Process, Queue


from .options import configs
logging.config.fileConfig(configs['logging'], disable_existing_loggers=False)

#logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

r_uuid = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

tasks = Queue()
ASPECT_LOOL = "lool:collaboraOnline"


class AlfrescoHandler(Process):
    """
    Handler that call Alfresco Server
    """

    def __init__(self, user, pwd, alf_ws="http://localhost:8080/alfresco/s/"):
        super(AlfrescoHandler, self).__init__()
        self.alf_ws = alf_ws if alf_ws[-1] != '/' else alf_ws[:-1]
        logger.info("Alfresco Handler connect to {}@{}".format(user, self.alf_ws))
        self.__user = user
        self.__pwd = pwd
        self.__ticket = None

    def ticket(self):
        if self.__ticket:
            query = "{}/api/login/ticket/{}".format(self.alf_ws, self.__ticket)
            logger.debug("alfresco_handler : query={}".format(query))
            r = requests.get(query,
                             params={'alf_ticket': self.__ticket})
            if r.ok:
                logger.debug("alfresco_handler : ticket ok !")
                return

        query = "{}/api/login.json".format(self.alf_ws)
        logger.debug("alfresco_handler : query={}".format(query))
        r_login = requests.get(query,
                               params={'u': self.__user, 'pw': self.__pwd})
        logger.debug("alfresco_handler : {}".format(r_login))

        if r_login.ok:
            data = r_login.json()
            logger.debug("alfresco_handler : {}".format(data['data']))
            self.__ticket = data['data']['ticket']
        else:
            raise HttpError(r_login)

    def adddoc(self, docKey):
        tasks.put(AddDocTask(docKey))

    def rmdoc(self, docKey):
        tasks.put(RmDocTask(docKey))

    def run(self):
        while True:
            logger.debug("alfresco_handler {} Wait for task"
                         .format(os.getpid()))
            task = tasks.get()
            if task is None:
                break
            task.do_work(self)

    def stop(self):
        tasks.put(None)

    def get_aspect(self, uuid):
        """Call list aspect webscript from Alfresco"""
        logger.debug("alfresco_handler->get_aspect")
        self.ticket()
        r_aspects = requests.get(
            "{}/slingshot/doclib/aspects/node/workspace/SpacesStore/{}"
            .format(self.alf_ws, uuid),
            params={'alf_ticket': self.__ticket}
        )
        logger.debug("alfresco_handler response {}".format(r_aspects.text))
        j_aspects = r_aspects.json()
        return j_aspects['current']

    def add_aspect(self, uuid, aspect):
        """Call add aspect webscript from Alfresco"""
        logger.debug("alfresco_handler->add_aspect")
        self.ticket()
        r_payload = requests.post(
            "{}/lool/aspect/add/workspace/SpacesStore/{}".format(self.alf_ws,
                                                                 uuid),
            params={'alf_ticket': self.__ticket},
            headers={"Content-type": "application/json",
                     "X-Requested-With": "application/x-www-form-urlencoded"}
        )
        logger.debug("alfresco_handler response {}".format(r_payload.text))
        return r_payload.ok

    def rm_aspect(self, uuid, aspect):
        """Call remove aspect webscript from Alfresco"""
        logger.debug("alfresco_handler->rm_aspect")
        self.ticket()
        r_payload = requests.post(
            "{}/lool/aspect/rem/workspace/SpacesStore/{}".format(self.alf_ws,
                                                                 uuid),
            params={'alf_ticket': self.__ticket},
            headers={"Content-type": "application/json",
                     "X-Requested-With": "application/x-www-form-urlencoded"}
        )
        logger.debug("alfresco_handler response {}".format(r_payload.text))
        return r_payload.ok

    def clean_version(self, uuid):
        """Call clean webscript from Alfresco"""
        logger.debug("alfresco_handler->rm_aspect")
        self.ticket()
        # Keep 10 last automatic versions
        r_payload = requests.post(
            "{}/lool/version/clean/workspace/SpacesStore/{}?keep_auto=10".format(self.alf_ws, uuid),
            params={'alf_ticket': self.__ticket},
            headers={"Content-type": "application/json"}
        )
        logger.debug("alfresco_handler response {}".format(r_payload.text))
        return r_payload.ok

class AddDocTask():
    """Task job that """
    def __init__(self, docKey=None):
        self.docKey = docKey

    def do_work(self, alfHandler):
        uuid = extractUuid(self.docKey)
        logger.info("alfresco_handler ADD DOC {}".format(uuid))
        aspects = alfHandler.get_aspect(uuid)
        if ASPECT_LOOL not in aspects:
            alfHandler.add_aspect(uuid, ASPECT_LOOL)


class RmDocTask():
    def __init__(self, docKey=None):
        self.docKey = docKey

    def do_work(self, alfHandler):
        uuid = extractUuid(self.docKey)
        logger.info("alfresco_handler RM DOC {}".format(uuid))
        aspects = alfHandler.get_aspect(uuid)
        if ASPECT_LOOL in aspects:
            alfHandler.rm_aspect(uuid, ASPECT_LOOL)
            alfHandler.clean_version(uuid)


def extractUuid(docKey):
    # /alfresco/s/wopi/files/a8290263-4178-48f5-a0b0-be155a424828
    matches = re.search(r_uuid, docKey)

    if matches:
        return matches.group()
    else:
        return None


class HttpError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, r):
        self.response = r
