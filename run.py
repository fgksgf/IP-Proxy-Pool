import logging
import sys

from proxypool.scheduler import Scheduler


def init_logger():
    """
    初始化日志器
    """
    logger = logging.getLogger('main')
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S')

    # 将日志输出到控制台
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    init_logger()
    schedule = Scheduler()
    schedule.run()
