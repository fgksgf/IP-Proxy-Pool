# Redis数据库地址
REDIS_HOST = 'redis'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'password'

# redis中存储代理的键名
REDIS_KEY = 'proxies'

# redis中存储锁的键名
LOCK_KEY = 'mutex_lock'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
DECREASE_SCORE = -10

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000

# 检查周期：一小时
TESTER_CYCLE = 60 * 60

# 获取周期：三小时
GETTER_CYCLE = 60 * 60 * 3

# 测试API，建议抓哪个网站测哪个
# 使用httpbin来判断代理是否为高匿代理
TEST_URL = 'http://httpbin.org/ip'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5000

# 代理测试器、代理获取器、API模块启用开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 代理测试器最大批测试量
BATCH_TEST_SIZE = 30
