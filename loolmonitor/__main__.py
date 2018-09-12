import logging
import logging.config
from multiprocessing import Process

from .options import configs
from .LoolMonitor import LoolMonitor
from .AlfrescoHandler import AlfrescoHandler


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)


def start_monitor(host=None, port=8765):
    monitor = LoolMonitor(configs['host'], configs['port'])
    alfHandler = AlfrescoHandler(configs['user'],
                                 configs['password'],
                                 configs['webscript'])
    alfHandler.start()
    monitor.work_handler.append(alfHandler)
    monitor.start()


if __name__ == '__main__':
    Process(target=start_monitor).start()
    logger.info("Monitor is started")
