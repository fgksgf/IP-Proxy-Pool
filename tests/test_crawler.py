import unittest
import re
from proxypool.crawler import Crawler


# TODO: Use decorator to refactor the code
class CrawlerTest(unittest.TestCase):
    crawler = Crawler()

    @staticmethod
    def get_number_of_proxies(proxies):
        count = 0
        try:
            p = next(proxies)
            while p:
                if re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', p):
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

    def test_crawl_proxylist(self):
        proxies = self.crawler.crawl_proxylist(max_page=1)
        self.assertGreater(self.get_number_of_proxies(proxies), 0)


if __name__ == '__main__':
    unittest.main()
