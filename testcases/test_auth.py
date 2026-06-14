# 测试需要登录的接口，编写需鉴权的接口测试（用户信息、购物车查询）验证接口关联问题

import allure
import pytest
from common.session_client import SessionClient
from common.yaml_util import read_yaml
from config.settings import BASE_URL, LOGIN_USERNAME, LOGIN_PASSWORD
import os

def get_auth_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, 'data', 'auth_data.yaml')
    data = read_yaml(yaml_path)
    return data.get('auth_tests', [])

@allure.feature("认证模块")
class TestAuthDataDriven:

    @pytest.fixture(scope="class")
    def valid_token_client(self):
        """获取一个有效的 token 客户端，供需要正常 token 的用例使用"""
        client = SessionClient(base_url=BASE_URL)
        resp = client.post("/auth/login", json={
            "username": LOGIN_USERNAME,
            "password": LOGIN_PASSWORD
        })
        assert resp.status_code == 200
        token = resp.json()["accessToken"]
        client.set_header("Authorization", f"Bearer {token}")
        return client

    @allure.story("认证接口数据驱动测试")
    @pytest.mark.parametrize("case", get_auth_cases(), ids=lambda x: x['name'])
    def test_auth_ddt(self, case, valid_token_client):
        # 根据用例标记，构建不同的客户端
        if case.get('use_invalid_token'):
            client = SessionClient(base_url=BASE_URL)
            client.set_header("Authorization", "Bearer invalid_token_123")
        elif case.get('no_token'):
            client = SessionClient(base_url=BASE_URL)
        elif case.get('use_bad_token_format'):
            client = SessionClient(base_url=BASE_URL)
            # 使用完全错误的 token 字符串
            client.set_header("Authorization", "abc123")
        else:
            # 默认使用有效 token 的客户端
            client = valid_token_client

        # 处理 endpoint 动态替换
        endpoint = case['endpoint']
        if case.get('dynamic_user_id'):
            me_resp = valid_token_client.get("/auth/me")
            assert me_resp.status_code == 200
            user_id = me_resp.json()['id']
            endpoint = endpoint.format(user_id=user_id)

        # 发送请求
        resp = client.get(endpoint)

        # 断言状态码
        assert resp.status_code == case['expected_status'], \
            f"用例 {case['name']} 状态码不符，预期 {case['expected_status']}，实际 {resp.status_code}"

        # 额外断言
        if case.get('check_username'):
            assert resp.json()['username'] == LOGIN_USERNAME
        if case.get('check_carts'):
            assert 'carts' in resp.json()