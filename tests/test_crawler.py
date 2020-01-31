import unittest
import re
from proxypool.crawler import Crawler


# TODO: Use decorator to refactor the code
class CrawlerTest(unittest.TestCase):
    """代理获取爬虫测试类

    测试各个代理源网站能否正常获取代理
    """

    crawler = Crawler()

    @staticmethod
    def get_number_of_proxies(proxies):
        """
        统计生成器中有效代理的数量

        :param proxies: 生成器
        :return: 代理数量
        """
        count = 0
        try:
            p = next(proxies)
            while p:
                if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', p):
                    count += 1
                    break
                p = next(proxies)
            return count
        except StopIteration:
            return count

    def test_crawl_xicidaili(self):
        proxies = self.crawler.crawl_xicidaili(max_page=1)
        self.assertGreater(self.get_number_of_proxies(proxies), 0)

    def test_crawl_ip3366(self):
        proxies = self.crawler.crawl_ip3366()
        self.assertGreater(self.get_number_of_proxies(proxies), 0)

    def test_crawl_qiyun(self):
        proxies = self.crawler.crawl_qiyun(max_page=1)
        self.assertGreater(self.get_number_of_proxies(proxies), 0)

    def test_crawl_xiaohuan(self):
        proxies = self.crawler.crawl_xiaohuan()
        self.assertGreater(self.get_number_of_proxies(proxies), 0)


if __name__ == '__main__':
    unittest.main()
