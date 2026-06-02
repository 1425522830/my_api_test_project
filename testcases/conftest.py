#  pytest的公共准备文件，定义全局 fixture，提供预登录的API客户端和数据库操作客户端。

import pytest
from common.session_client import SessionClient
from common.db_util import DBClient
from config.settings import BASE_URL, LOGIN_USERNAME, LOGIN_PASSWORD

@pytest.fixture(scope="session")
def api_client():
    # session 级别夹具：登录一次，返回带 token 的 SessionClient
    client = SessionClient(base_url=BASE_URL)
    login_resp = client.post("/auth/login", json={
        "username": LOGIN_USERNAME,
        "password": LOGIN_PASSWORD
    })
    assert login_resp.status_code == 200, "登录失败"
    token = login_resp.json()["accessToken"]
    client.set_header("Authorization", f"Bearer {token}")
    return client

@pytest.fixture(scope="function")
def db_client():
    # 每个测试函数独立的数据库连接，自动关闭
    client = DBClient()
    yield client
    client.close()