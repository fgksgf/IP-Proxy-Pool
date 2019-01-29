# Redis数据库地址
REDIS_HOST = '119.29.135.136'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'iE23fP$d9yTQCgmc'

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
DECREASE_SCORE = -1

VALID_STATUS_CODES = [200, ]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 5000

# 检查周期：一小时
TESTER_CYCLE = 60 * 60
# 获取周期：三小时
GETTER_CYCLE = 60 * 60 * 3

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'https://www.jd.com/'

# API配置
API_HOST = '127.0.0.1'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 20