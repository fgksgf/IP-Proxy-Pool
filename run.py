import logging
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
    print(redis.get_proxy_count())
    print(redis.random_get_proxy())


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
    logger.setLevel(level=logging.DEBUG)

    # Handler
    handler = logging.FileHandler('result.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == '__main__':
    init_logger()
    schedule = Scheduler()
    schedule.run()
    # test_database()
    # test_tester()
