import logging
import sys

from proxypool.database import RedisClient
from proxypool.getter import Getter
from proxypool.scheduler import Scheduler
from proxypool.tester import Tester
from proxypool.api import app


def test_database():
    """
    测试数据库IO模块
    """
    redis = RedisClient()
    redis.db.set('test', 1)
    print(redis.db.get('test'))
    redis.db.set('test', 2)
    print(type(redis.db.get('test')))


def test_getter():
    """
    测试代理获取器模块
    """
    getter = Getter()
    getter.run()


def test_tester():
    """
    测试代理测试器模块
    """
    tester = Tester()
    tester.run()


def test_api():
    """
    测试API模块
    """
    app.run()


def init_logger():
    """
    初始化日志器
    """
    logger = logging.getLogger('main')
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 将日志输出到控制台
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    init_logger()
    schedule = Scheduler()
    schedule.run()
    # test_database()
    # test_tester()
