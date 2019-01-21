from proxypool.database import RedisClient
from proxypool.getter import Getter
from proxypool.scheduler import Scheduler
from proxypool.tester import Tester
from proxypool.api import app


def test_database():
    redis = RedisClient()
    print(redis.get_proxy_count())
    print(redis.random_get_proxy())
    print(redis.random_get_proxy())
    print(redis.random_get_proxy())


def test_getter():
    getter = Getter()
    getter.run()


def test_tester():
    tester = Tester()
    tester.run()


def test_api():
    app.run()


if __name__ == '__main__':
    schedule = Scheduler()
    schedule.run()
    # test_database()
    # test_tester()
