import asyncio
import aiohttp
import time

from .database import RedisClient
from .setting import *


class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy, timeout=5.0):
        """
        测试单个代理
        :param timeout: 测试代理的最大等待时长，默认为5秒
        :param proxy: 需要测试的代理
        :return:
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
                        # print('代理不可用: ', proxy, response.status)
            except Exception as e:
                self.redis.degrade_proxy(proxy)
                print('ERROR: ', e.args)

    def run(self, sleep_time=3):
        """
        测试主函数
        :param sleep_time: 批测试间隔时间，默认为5秒
        :return:
        """
        print('-' * 10, '测试器开始运行', '-' * 10)
        try:
            count = self.redis.get_proxy_count()
            print('当前剩余: ', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理...')
                test_proxies = self.redis.get_batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(sleep_time)
        except Exception as e:
            print('测试器发生错误: ', e.args)
