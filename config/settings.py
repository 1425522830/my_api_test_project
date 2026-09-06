import os
from dotenv import load_dotenv

load_dotenv()                   # 加载.env文件的账号和密码

BASE_URL = os.getenv("BASE_URL", "https://www.wangdanatest.top")
TEST_ACCOUNT = os.getenv("TEST_ACCOUNT", "")
TEST_PWD = os.getenv("TEST_PWD", "")

TEST_ACCOUNT_B = os.getenv("TEST_ACCOUNT_B", "")
TEST_PWD_B = os.getenv("TEST_PWD_B", "")


BASE_HEADERS = {"Content-Type": "application/json; charset=utf-8"}
REQ_TIMEOUT = 10

VERIFY_SSL = False                      # 防止这个网站的证书不安全，使得Python直接拒绝连接

API_LOGIN = "/login"
API_REGISTER = "/register"
API_FORGOT = "/api/forgot"
API_USERS = "/api/users"
API_ACCESS_TOKENS = "/api/access-tokens"
API_SESSIONS = "/api/sessions"
API_AVATAR = "/avatar"
API_POSTS = "/api/posts"
API_DISCUSSIONS = "/api/discussions"