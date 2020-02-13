import json
import logging
from flask import Flask, g
from .database import RedisClient

__all__ = ['app']
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h1>Welcome to IP Proxy Pool.</h1>'


@app.route('/random')
def get_single_proxy():
    """
    随机获取一个可用代理

    :return: 随机代理
    """
    conn = get_conn()
    return str(conn.random_get_proxy())


@app.route('/batch')
def get_batch_proxy():
    """
    获取当前所有可用代理

    :return: 可用代理列表
    """
    conn = get_conn()
    return json.dumps(conn.get_all_available())


@app.route('/count')
def get_counts():
    """
    返回当前代理池中代理数量

    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.get_proxy_count())
