# 配置文件，集中管理测试配置（基础URL、测试账号、公共请求头、数据库连接参数）

BASE_URL = "https://dummyjson.com"          # 公共url

LOGIN_USERNAME = "emilys"                   # 测试专用账号密码
LOGIN_PASSWORD = "emilyspass"

HEADERS = {
    "Content-Type": "application/json"      # 请求头
}

# 数据库配置（mysql）
DATABASE = {
    'type': 'mysql',
    'host': 'localhost',        # MySQL地址
    'port': 3306,               # 默认端口
    'user': 'root',             # 用户名
    'password': '123456',       # 密码
    'database': 'test_db',      # 数据库名
    'charset': 'utf8mb4'
}

# 设置超时,防止永久阻塞
REQUEST_TIMEOUT = 10