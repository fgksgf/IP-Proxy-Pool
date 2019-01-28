import asyncio
import logging

import aiohttp
import time

from .database import RedisClient
from .setting import *


class Tester:
    def __init__(self):
        self.redis = RedisClient()
        self.logger = logging.getLogger('main.tester')

    async def test_single_proxy(self, proxy, timeout=5.0):
        """
        测试单个代理
        :param timeout: 测试代理的最大等待时长，默认为5秒
        :param proxy: 需要测试的代理
        """
        async with aiohttp.ClientSession() as session:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            try:
                async with session.get(TEST_URL, proxy=real_proxy, timeout=timeout) as response:
                    if response.status == 200:
                        self.redis.set_max_score(proxy)
                    else:
                        self.redis.degrade_proxy(proxy)
            except Exception as e:
                self.redis.degrade_proxy(proxy)
                self.logger.error('测试单个代理异常: ', e.args)

    def run(self, sleep_time=5):
        """
        测试主函数
        :param sleep_time: 批测试间隔时间，默认为5秒
        """
        self.logger.info('测试器开始运行')
        try:
            count = self.redis.get_proxy_count()
            self.logger.info('当前剩余: ', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                self.logger.info('正在测试第', start + 1, '-', stop, '个代理...')
                test_proxies = self.redis.get_batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(sleep_time)
        except Exception as e:
            self.logger.error('测试器异常: ', e.args)
