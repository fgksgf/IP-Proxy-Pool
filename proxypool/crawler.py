import logging
import random
import time

import requests
from pyquery import PyQuery as pq

from requests.exceptions import ConnectionError
from random_useragent.random_useragent import Randomize

r_agent = Randomize()
platform = ['windows', 'mac', 'linux']

headers = {
    'User-Agent': '',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


class ProxyMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(mcs, name, bases, attrs)


# TODO: Refactor code to reduce duplicated code.
class Crawler(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.logger = logging.getLogger('main.crawler')

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def get_page(self, url):
        random_user_agent = r_agent.random_agent('desktop', random.choice(platform))
        headers['User-Agent'] = random_user_agent
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            self.logger.error('抓取失败: %s %s', url, response.status_code)
            return None

    def crawl_xicidaili(self, max_page=10):
        """
        抓取西刺国内高匿代理IP

        :param max_page: 每页100条数据，要抓取的最大页数，默认为10
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        count = 0
        base_url = 'https://www.xicidaili.com/nn/{page}'
        for i in range(1, max_page + 1):
            url = base_url.format(page=i)
            html = self.get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr')

                # 因为第一行表头也是tr，所以采用这种方式，而不是遍历trs
                for j in range(1, 101):
                    # ip地址
                    ip_address = trs.eq(j).children('td').eq(1).text().strip()
                    # 端口
                    port = trs.eq(j).children('td').eq(2).text().strip()
                    if ip_address and port:
                        count += 1
                        yield ip_address + ':' + port

        self.logger.info('西刺代理: 共爬取 %d 条代理', count)

    def crawl_ip3366(self):
        """
        抓取IP3366网站国内高匿代理

        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        count = 0
        base_url = 'http://www.ip3366.net/free/?stype=1&page={page}'
        for page in range(1, 7):
            url = base_url.format(page=page)
            html = self.get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.table tr')
                for i in range(1, 16):
                    # ip地址
                    ip_address = trs.eq(i).children('td').eq(0).text().strip()
                    # 端口
                    port = trs.eq(i).children('td').eq(1).text().strip()
                    if ip_address and port:
                        count += 1
                    yield ip_address + ':' + port
        self.logger.info('IP3366: 共爬取 %d 条代理', count)

    def crawl_qiyun(self, max_page=10):
        """
        抓取齐云代理网站国内高匿代理

        :param max_page: 每页10条数据，要抓取的最大页数，默认为10
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        count = 0
        base_url = 'https://www.7yip.cn/free/?action=china&page={page}'
        for page in range(1, max_page + 1):
            url = base_url.format(page=page)
            html = self.get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.table tbody tr')
                for i in range(0, 10):
                    count += 1
                    # ip地址
                    ip_address = trs.eq(i).children('td').eq(0).text().strip()
                    # 端口
                    port = trs.eq(i).children('td').eq(1).text().strip()
                    yield ip_address + ':' + port
        self.logger.info('齐云代理: 共爬取 %d 条代理', count)

    def crawl_xiaohuan(self):
        """
        抓取小幻代理网站的国内高匿代理，每小时更新一次

        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        base_url = 'https://ip.ihuan.me/today/{date}.html'
        date_str = time.strftime("%Y/%m/%d/%H", time.localtime())
        count = 0
        url = base_url.format(date=date_str)
        html = self.get_page(url)
        if html:
            doc = pq(html)
            items = doc('.text-left').text().strip().split('\n')
            for item in items:
                if item.find('高匿') != -1:
                    count += 1
                    p = item.find('@')
                    proxy = item[:p]
                    yield proxy
        self.logger.info('小幻代理: 共爬取 %d 条代理', count)


if __name__ == '__main__':
    crawler = Crawler()
    # print(next(crawler.crawl_xicidaili(max_page=1)))
    # print(next(crawler.crawl_xiaohuan()))
