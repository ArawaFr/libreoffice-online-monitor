import logging
from multiprocessing import Process
from LoolMonitor import LoolMonitor


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger = logging.getLogger('loolmonitor')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

def start_monitor(host='127.0.0.1', port=8765):
    monitor = LoolMonitor(host, port)
    monitor.start()

if __name__ == '__main__':
    Process(target=start_monitor).start()
    logger.info ("Monitor is started")
