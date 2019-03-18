import logging

from .database import RedisClient
from .crawler import Crawler
from .setting import *


class Getter:
    """代理获取器

    运行爬虫从各代理网站爬取代理数据，并存储到redis数据库
    """

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
        self.logger = logging.getLogger('main.getter')

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
        self.logger.info('获取器开始运行')
        # 在redis中设置获取器运行状态标志
        self.redis.db.set('getter:status', 'work')
        count = 0
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                count += len(proxies)
                self.redis.add_proxies(proxies)
            self.logger.info('获取器共爬取：' + str(count) + '条代理')
        # 在redis中更改获取器运行状态标志，0表示空闲中
        self.redis.db.set('getter:status', 'idle')
