# 测试登录接口（数据驱动），对登录接口进行参数化测试，覆盖正向与异常场景。

import allure
import pytest
from config.settings import BASE_URL
from common.yaml_util import get_login_data
from common.session_client import SessionClient

@allure.feature("登录模块")
class TestLoginDDT:
    @allure.story("登录接口数据驱动测试")
    @pytest.mark.parametrize("case", get_login_data())
    def test_login(self, case):
        with allure.step(f"准备测试数据: {case['name']}"):
            payload = {}                # 动态构建请求体，只包含存在的字段
            if "username" in case:
                payload["username"] = case["username"]
            if "password" in case:
                payload["password"] = case["password"]

            expected_status = case["expected_status"]
            expected_message = case.get("expected_message", None)
            expect_token = case.get("expect_token", False)

        with allure.step("发送登录请求"):
            client = SessionClient(base_url=BASE_URL)
            resp = client.post("/auth/login", json=payload)     # 如果两个字段都不存在，payload 为空对象，API 应返回 400

        with allure.step("校验状态码"):
            assert resp.status_code == expected_status, f"用例 {case['name']} 状态码不符"

        if expect_token:
            with allure.step("校验返回 token"):
                resp_json = resp.json()
                assert "accessToken" in resp_json, "登录成功但未返回 token"
                assert resp_json["accessToken"], "token 为空"
        elif expected_message is not None:
            with (allure.step("校验返回消息")):
                resp_json = resp.json()
                actual_msg = resp_json.get("message", "")
                # 忽略大小写和首尾空格（给编写用例留有容错）
                assert expected_message.lower().strip() == actual_msg.lower().strip(),  \
                    f"预期消息：{expected_message}，实际：{actual_msg}"

        allure.attach(str(resp.json()), name="响应内容", attachment_type=allure.attachment_type.JSON)