import logging
import config

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
    alfHandler = AlfrescoHandler(
                    config.ALFRESCO_CONFIG['user'],
                    config.ALFRESCO_CONFIG['password'],
                    config.ALFRESCO_CONFIG['host'],
                    ssl=config.ALFRESCO_CONFIG['ssl']
    )
    alfHandler.start()
    monitor.work_handler.append(alfHandler)
    monitor.start()

if __name__ == '__main__':
    Process(target=start_monitor).start()
    logger.info ("Monitor is started")
