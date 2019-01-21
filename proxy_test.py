import json

import requests

# TEST_URL = 'http://httpbin.org/get'

proxy_lst = ["61.142.72.154:48404",
             "47.90.73.118:3128",
             "183.63.123.3:56489"]

if __name__ == '__main__':
    for proxy in proxy_lst:
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            response = requests.get('https://www.jd.com/', proxies=proxies)
            response.raise_for_status()
            # print("ok")
            # print(response.text)
        except Exception as e:
            print(e.args)
        # if response.status_code == 200:
        # js = json.loads(response.text)
        # print(response.text)
