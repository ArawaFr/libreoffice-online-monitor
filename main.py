import logging
from multiprocessing import Process
from LoolMonitor import LoolMonitor
from CmisHandler import CmisHandler


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
    cmisHandler = CmisHandler()
    cmisHandler.start()
    monitor.work_handler.append(cmisHandler)
    monitor.start()

if __name__ == '__main__':
    Process(target=start_monitor).start()
    logger.info ("Monitor is started")
