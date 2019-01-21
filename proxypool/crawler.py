import random
import time

import requests
from pyquery import PyQuery as pq

from requests.exceptions import ConnectionError
from random_useragent.random_useragent import Randomize

r_agent = Randomize()
platform = ['windows', 'mac', 'linux']

base_headers = {
    'User-Agent': '',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    random_user_agent = r_agent.random_agent('desktop', random.choice(platform))
    base_headers['User-Agent'] = random_user_agent
    headers = dict(base_headers, **options)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败: ', url, response.status_code)
        return None


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


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_xicidaili(self, max_page=10):
        """
        抓取西刺国内高匿代理IP
        :param max_page: 每页100条数据，要抓取的最大页数，默认为10
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        print('正在爬取西刺代理...')
        count = 0
        base_url = 'https://www.xicidaili.com/nn/{page}'
        for i in range(1, max_page + 1):
            url = base_url.format(page=i)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr')
                for j in range(1, 101):
                    # 存活时间
                    live_time = trs.eq(j).children('td').eq(8).text().strip()
                    if '天' in live_time:
                        count += 1
                        # ip地址
                        ip_address = trs.eq(j).children('td').eq(1).text().strip()
                        # 端口
                        port = trs.eq(j).children('td').eq(2).text().strip()
                        yield ip_address + ':' + port
        print('共爬取', count, '条代理\n\n')

    def crawl_ip3366(self):
        """
        抓取IP3366网站国内高匿代理
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        print('正在爬取IP3366代理...')
        count = 0
        base_url = 'http://www.ip3366.net/free/?stype=1&page={page}'
        for page in range(1, 7):
            url = base_url.format(page=page)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.table tr')
                for i in range(1, 16):
                    count += 1
                    # ip地址
                    ip_address = trs.eq(i).children('td').eq(0).text().strip()
                    # 端口
                    port = trs.eq(i).children('td').eq(1).text().strip()
                    yield ip_address + ':' + port
        print('共爬取', count, '条代理\n\n')

    def crawl_iphai(self):
        """
        抓取IP海网站国内高匿代理
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        print('正在爬取IP海代理...')
        count = 0
        url = 'http://www.iphai.com/free/ng'
        html = get_page(url)
        if html:
            doc = pq(html)
            trs = doc('.table tr')
            for i in range(1, 17):
                count += 1
                # ip地址
                ip_address = trs.eq(i).children('td').eq(0).text().strip()
                # 端口
                port = trs.eq(i).children('td').eq(1).text().strip()
                yield ip_address + ':' + port
        print('共爬取', count, '条代理\n\n')

    def crawl_data5u(self):
        """
        抓取DATA5U网站国内高匿代理
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        print('正在爬取无忧代理...')
        count = 0
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(url)
        if html:
            doc = pq(html)
            uls = doc('.wlist .l2')
            for i in range(0, 15):
                count += 1
                # ip地址
                ip_address = uls.eq(i).children('span').eq(0).text().strip()
                # 端口
                port = uls.eq(i).children('span').eq(1).text().strip()
                yield ip_address + ':' + port
        print('共爬取', count, '条代理\n\n')

    def crawl_qiyun(self, max_page=10):
        """
        抓取旗云代理网站国内高匿代理
        :param max_page: 每页10条数据，要抓取的最大页数，默认为10
        :return: 返回代理字符串，格式为'ip地址:端口'
        """
        print('正在爬取旗云代理...')
        count = 0
        base_url = 'http://www.qydaili.com/free/?page={page}'
        for page in range(1, max_page + 1):
            url = base_url.format(page=page)
            html = get_page(url)
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
        print('共爬取', count, '条代理\n\n')

    def crawl_xiaohuan(self):
        print('正在爬取小幻代理...')
        base_url = 'https://ip.ihuan.me/today/{date}.html'
        date_str = time.strftime("%Y/%m/%d/%H", time.localtime())
        count = 0
        url = base_url.format(date=date_str)
        html = get_page(url)
        if html:
            doc = pq(html)
            items = doc('.text-left').text().strip().split('\n')
            for item in items:
                if item.find('高匿') != -1:
                    count += 1
                    p = item.find('@')
                    proxy = item[:p]
                    yield proxy
        print('共爬取', count, '条代理\n\n')


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_66ip()
    # crawler.crawl_xiaohuan()
    # crawler.crawl_qiyun()
    # crawler.crawl_data5u()
    # crawler.crawl_iphai()
    # crawler.crawl_ip3366()
    # crawler.crawl_xicidaili()
