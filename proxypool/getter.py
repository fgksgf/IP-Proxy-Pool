import logging

from proxypool.database import RedisClient
from proxypool.crawler import Crawler
from proxypool.settings import *


class Getter:
    """代理获取器

    运行爬虫从各代理网站爬取代理数据，并存储到redis数据库
    """

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
        self.logger = logging.getLogger('getter')

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return: 若代理数量达到上限，则返回True，否则返回False
        """
        return self.redis.get_proxy_count() >= POOL_UPPER_THRESHOLD

    def run(self):
        """
        调用爬虫中的一系列函数，爬取代理，并将代理保存到数据库
        :return: 返回爬取的所有代理数量
        """
        self.logger.info('start running')
        # 在redis中设置获取器运行状态标志
        self.redis.redis.set('getter:status', 'work')

        if not self.is_over_threshold():
            count = 0
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                count += len(proxies)
                self.redis.add_proxies(proxies)
            self.logger.info('共爬取：%d条代理', count)

        # 在redis中更改获取器运行状态标志
        self.redis.redis.set('getter:status', 'idle')
        self.logger.info('运行结束，进入等待状态')
