import logging
from multiprocessing import Process
from LoolMonitor import LoolMonitor
from AlfrescoHandler import AlfrescoHandler


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger = logging.getLogger('loolmonitor')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

def start_monitor(host=None, port=8765):
    monitor = LoolMonitor(host, port)
    alfHandler = AlfrescoHandler(usr, pwd, "alfresco:8080", ssl=False)
    alfHandler.start()
    monitor.work_handler.append(alfHandler)
    monitor.start()

if __name__ == '__main__':
    Process(target=start_monitor).start()
    logger.info ("Monitor is started")
