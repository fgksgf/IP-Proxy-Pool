import asyncio
import logging

import aiohttp
import time

from proxypool.database import RedisClient
from proxypool.settings import *


class Tester:
    def __init__(self):
        self.redis = RedisClient()
        self.logger = logging.getLogger('main.tester')

    @staticmethod
    def check_anonymity(proxy, result):
        """
        检测代理是否为高匿代理

        :param proxy: 代理
        :param result: 测试URL返回的json结果
        :return: 若为高匿代理返回True，否则返回False
        """
        ret = False
        origin = result.get('origin').split(', ')
        # 若为高匿代理会返回两个相同的代理ip
        if len(origin) == 2 and proxy in origin:
            ret = True
        return ret

    async def test_single_proxy(self, proxy, timeout=7.0):
        """
        测试单个代理

        :param timeout: 测试代理的最大等待时长，默认为7秒
        :param proxy: 需要测试的代理
        """
        async with aiohttp.ClientSession() as session:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            try:
                async with session.get(TEST_URL, proxy=real_proxy, timeout=timeout) as response:
                    if response.status == 200:
                        json_result = await response.json()
                        if self.check_anonymity(proxy, json_result):
                            self.redis.set_max_score(proxy)
                    else:
                        self.redis.degrade_proxy(proxy)
            except Exception:
                self.redis.degrade_proxy(proxy)

    def run(self, sleep_time=5):
        """
        批量测试代理

        :param sleep_time: 批测试间隔时间，默认为5秒
        """
        if self.redis.acquire_lock():
            self.logger.info('开始测试代理')
            count = self.redis.get_proxy_count()
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                try:
                    test_proxies = self.redis.get_batch(start, stop)
                    loop = asyncio.get_event_loop()
                    tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                    loop.run_until_complete(asyncio.wait(tasks))
                    time.sleep(sleep_time)
                except Exception:
                    self.logger.error('测试第 %d-%d个代理出错', start + 1, stop)
            self.redis.release_lock()
