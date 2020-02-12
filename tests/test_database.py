from unittest import TestCase

from proxypool.database import RedisClient


class TestRedisClient(TestCase):
    def test_add_proxies(self):
        redis = RedisClient()
        test_data = [str(i) for i in range(100)]
        ret = redis.add_proxies(test_data, key='test')
        self.assertEqual(len(test_data), ret)
