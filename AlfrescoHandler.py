#!/usr/bin/env python
import os
import logging
from multiprocessing import Process, Queue
import queue
import re, json, urllib
import http.client

logger = logging.getLogger(__name__)

r_uuid = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

tasks = Queue()
ASPECT_LOOL="lool:collaboraOnline"

class AlfrescoHandler(Process):
    """
    Handler that call Alfresco Server
    """

    def __init__(self, user, pwd, wsUrl="localhost:8080", ssl=True):
        super(AlfrescoHandler, self).__init__()
        if ssl:
            self.conn = http.client.HTTPSConnection(wsUrl)
        else:
            self.conn = http.client.HTTPConnection(wsUrl)


        self.conn.request("GET","/alfresco/s/api/login.json?u={}&pw={}".format(user, pwd))
        r_login = self.conn.getresponse()
        data = json.loads(r_login.read())
        logger.debug ("+++alfHandler+++ {}".format(data['data']))
        self.ticket = data['data']['ticket']
        self.conn.close()


        #params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
        self.conn.request("GET", "/alfresco/s/api/people/admin/preferences?alf_ticket={}".format(self.ticket))
        r_pref = self.conn.getresponse()
        logger.debug ("+++alfHandler+++ {}".format(r_pref.read()))
        self.conn.close()

        # test a8290263-4178-48f5-a0b0-be155a424828
        uuid = extractUuid("/alfresco/s/wopi/files/a8290263-4178-48f5-a0b0-be155a424828")
        logger.info ("+++alfHandler+++ ADD DOC {}".format(uuid))
        aspects = self.get_aspect(uuid)
        if not ASPECT_LOOL in aspects:
            self.add_aspect(uuid, ASPECT_LOOL)


    def adddoc(self, docKey):
        tasks.put(AddDocTask(docKey))

    def rmdoc(self, docKey):
        tasks.put(RmDocTask(docKey))

    def run(self):
        while True:
            logger.debug ("+++alfHandler+++ {} Wait for task".format(os.getpid()))
            task = tasks.get()
            if task is None:
                break
            task.do_work(self)

    def stop(self):
        tasks.put(None)

    def get_aspect(self, uuid):
        # https://my-alfresco.jeci.fr/share/proxy/alfresco/slingshot/doclib/aspects/node/workspace/SpacesStore/a8290263-4178-48f5-a0b0-be155a424828
        try:
            query = "/alfresco/s/slingshot/doclib/aspects/node/workspace/SpacesStore/{}?alf_ticket={}".format(uuid, self.ticket)
            self.conn.request("GET", query)

            logger.debug ("+++alfHandler+++ query {}".format(query))
            r_aspects = self.conn.getresponse()
            j_aspects = json.loads(r_aspects.read())
            return j_aspects['current']
        finally:
            self.conn.close()

    def add_aspect(self, uuid, aspect):
        try:
            #
            query = "/alfresco/s/slingshot/doclib/action/aspects/node/workspace/SpacesStore/{}?alf_ticket={}".format(uuid, self.ticket)
            body = json.dumps({"added" : [ aspect ], "removed" : []})
            logger.debug ("+++alfHandler+++ query {} + {}".format(query, body))
            headers = { "Content-type": "application/json",
                        "X-Requested-With": "application/x-www-form-urlencoded"}

            self.conn.request("POST", query, body, headers)

            r_payload = self.conn.getresponse()
            logger.debug ("+++alfHandler+++ response {}".format(r_payload.read()))
            return r_payload
        finally:
            self.conn.close()

    def rm_aspect(self, uuid, aspect):
        try:
            query = "/alfresco/s/slingshot/doclib/action/aspects/node/workspace/SpacesStore/{}?alf_ticket={}".format(uuid, self.ticket)
            body = json.dumps({"added" : [], "removed" : [ aspect ]})
            logger.debug ("+++alfHandler+++ query {} + {}".format(query, body))
            headers = { "Content-type": "application/json",
                        "X-Requested-With": "application/x-www-form-urlencoded"}
            self.conn.request("POST", query, body, headers)
            r_payload = self.conn.getresponse()
            logger.debug ("+++alfHandler+++ response {}".format(r_payload.read()))
            return r_payload
        finally:
            self.conn.close()


class AddDocTask():
    def __init__(self, docKey=None):
        self.docKey = docKey

    def do_work(self, alfHandler):
        uuid = extractUuid(self.docKey)
        logger.info ("+++alfHandler+++ ADD DOC {}".format(uuid))
        aspects = alfHandler.get_aspect(uuid)
        if not ASPECT_LOOL in aspects:
            alfHandler.add_aspect(uuid, ASPECT_LOOL)


class RmDocTask():
    def __init__(self, docKey=None):
        self.docKey = docKey

    def do_work(self, alfHandler):
        uuid = extractUuid(self.docKey)
        logger.info ("+++alfHandler+++ RM DOC {}".format(uuid))
        aspects = alfHandler.get_aspect(uuid)
        if ASPECT_LOOL in aspects:
            alfHandler.rm_aspect(uuid, ASPECT_LOOL)



def extractUuid(docKey):
    # /alfresco/s/wopi/files/a8290263-4178-48f5-a0b0-be155a424828
    matches = re.search(r_uuid, docKey)

    if matches:
        return matches.group()
    else:
        return None
