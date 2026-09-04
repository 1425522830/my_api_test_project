import allure
import pytest
from api.user_api import UserApi
from common.yaml_util import get_login_case, get_register_case, get_forgot_pwd_case

@allure.feature("用户模块")
@allure.story("账户认证")
class TestLoginDDT:
    @allure.story("登录接口数据驱动测试")
    @pytest.mark.parametrize("case", get_login_case(), ids=lambda x: x["case_name"])  # 修正为 case_name
    def test_login_interface(self, case, raw_client):
        user_api = UserApi(raw_client)
        account = case["identification"]
        pwd = case["password"]
        rem = case["remember"]
        expect_code = case["expect_status"]
        expect_msg = case.get("expect_msg", "")
        with allure.step(f"执行测试用例：{case['case_name']}"):
            res = user_api.login(account, pwd, rem)
        with allure.step("校验接口响应状态码"):
            assert res.status_code == expect_code, f"预期状态码{expect_code}，实际{res.status_code}"
        if expect_msg:
            with allure.step("校验返回提示信息"):
                assert expect_msg in res.text
        allure.attach(res.text, "接口完整返回数据", allure.attachment_type.TEXT)


@allure.feature("用户模块")
@allure.story("账户认证")
class TestRegisterDDT:
    @allure.story("注册接口数据驱动测试")
    @pytest.mark.parametrize("case", get_register_case(), ids=lambda x: x["case_name"])
    def test_register_interface(self, case, raw_client):
        user_api = UserApi(raw_client)
        username = case["username"]
        email = case["email"]
        password = case["password"]
        nickname = case["nickname"]
        expect_code = case["expect_status"]
        expect_msg = case.get("expect_msg", "")
        with allure.step(f"执行注册用例：{case['case_name']}"):
            resp = user_api.register(username, email, password, nickname)
        with allure.step("校验接口响应状态码"):
            assert resp.status_code == expect_code, f"预期状态码{expect_code}，实际{resp.status_code}"
        if expect_msg:
            with allure.step("校验返回提示信息"):
                assert expect_msg in resp.text
        allure.attach(resp.text, "注册接口返回数据", allure.attachment_type.TEXT)


@allure.feature("用户模块")
@allure.story("账户认证")
class TestForgotPwd:
    @allure.story("忘记密码/重置密码邮件发送测试")
    @pytest.mark.parametrize("case", get_forgot_pwd_case(), ids=lambda x: x["case_name"])
    def test_forgot_password_email(self, case, raw_client):
        user_api = UserApi(raw_client)
        email = case["email"]
        expect_code = case["expect_status"]
        with allure.step(f"执行发送重置密码邮件：{case['case_name']}"):
            resp = user_api.send_forgot_pwd_email(email)
        with allure.step("校验接口响应状态码"):
            assert resp.status_code == expect_code, f"预期状态码{expect_code}，实际{resp.status_code}"
        allure.attach(f"请求邮箱：{email}\n响应状态码：{resp.status_code}", "接口请求与返回简要信息", allure.attachment_type.TEXT)