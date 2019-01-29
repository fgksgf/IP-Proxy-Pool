import redis

from .error import PoolEmptyError
from .setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from .setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE, DECREASE_SCORE
from random import choice

import re


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add_proxies(self, proxies, score=INITIAL_SCORE):
        """
        使用管道，批量向数据库中添加代理数据，将其分数设置为最高
        :param proxies: 代理
        :param score: 分数
        :return: 添加结果
        """
        with self.db.pipeline(transaction=False) as pipe:
            for proxy in proxies:
                if re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
                    pipe.zadd(REDIS_KEY, {proxy: score})
            pipe.execute()

    def random_get_proxy(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        # 获取分数大于等于100的代理
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, '+inf')
        if len(result):
            return choice(result)
        else:
            # 获无符合条件的代理，则获取分数大于等于初始分数的代理
            result = self.db.zrevrangebyscore(REDIS_KEY, '+inf', INITIAL_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def degrade_proxy(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            return self.db.zincrby(REDIS_KEY, DECREASE_SCORE, proxy)
        else:
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断数据库中是否存在某代理
        :param proxy: 代理
        :return: 是否存在，
        """
        return not (self.db.zscore(REDIS_KEY, proxy) is None)

    def set_max_score(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def get_proxy_count(self):
        """
        获取数据库中的代理数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def get_all_ascending(self):
        """
        获取全部代理，按分数升序
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def get_batch(self, start, stop):
        """
        从数据库中批量获取代理
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

    def get_all_available(self):
        """
        从数据库中获取所有可用代理
        :return: 代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, '+inf')
