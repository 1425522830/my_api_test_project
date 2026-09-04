import allure
import pytest
import os
from common.yaml_util import (
    get_user_info_cases,
    get_user_settings_cases,
    get_notification_privacy_cases,
    get_security_cases
)


# ------------------------------------------------
# 个人中心-信息查询
# ------------------------------------------------
@allure.feature("个人信息管理")
class TestUserTabQuery:
    @allure.story("个人页面 Tab 列表查询")
    @pytest.mark.parametrize("case", get_user_info_cases(), ids=lambda x: x["case_name"])
    def test_tab_list_query(self, login_client, case):
        api, current_uid = login_client
        allure.attach(str(current_uid), "当前登录账号 UID", allure.attachment_type.TEXT)

        if case["operate"] == "get_my_replies":
            resp = api.client.get(f"/api/posts?filter[author]={current_uid}")
        elif case["operate"] == "get_my_discussions":
            resp = api.client.get(f"/api/discussions?filter[author]={current_uid}")
        else:
            # 其他操作兜底接口
            resp = api.client.get(f"/api/users/{current_uid}")

        assert resp.status_code == case["expect_status"]

        # 防御式断言，防止假成功
        json_resp = resp.json()
        assert "data" in json_resp, f"接口返回 200，但缺少 data 字段！实际返回为：{json_resp}"


# ------------------------------------------------
# 个人中心-昵称/简介修改
# ------------------------------------------------
@allure.feature("个人信息管理")
class TestUserSettings:
    @allure.story("更改个人资料/昵称")
    @pytest.mark.parametrize("case", get_user_settings_cases(), ids=lambda x: x["case_name"])
    def test_update_user_nickname(self, login_client, case):
        api, current_uid = login_client
        allure.attach(f"当前用户 ID: {current_uid}", "前置条件", allure.attachment_type.TEXT)

        nickname = case["nickname"]
        bio = case["bio"]
        expect_code = case["expect_status"]

        with allure.step(f"执行更改资料用例：{case['case_name']}"):
            resp = api.update_user_profile(current_uid, nickname=nickname, bio=bio)

        with allure.step("校验接口响应状态码"):
            assert resp.status_code == expect_code, f"预期状态码{expect_code}，实际{resp.status_code}"

        allure.attach(resp.text, "修改资料接口返回数据", allure.attachment_type.TEXT)


# ------------------------------------------------
# 个人中心-通知与隐私设置
# ------------------------------------------------
@allure.feature("个人信息管理")
class TestNotificationAndPrivacy:
    @allure.story("通知中心及隐私设置开关")
    @pytest.mark.parametrize("case", get_notification_privacy_cases(), ids=lambda x: x["case_name"])
    def test_toggle_notification_and_privacy(self, login_client, case):
        api, current_uid = login_client
        preferences_dict = {case["preference_key"]: case["preference_value"]}

        with allure.step(f"切换设置：{case['case_name']}"):
            resp = api.update_user_preferences(current_uid, preferences_dict)

        with allure.step("校验接口响应状态码"):
            assert resp.status_code == case[
                "expect_status"], f"预期状态码{case['expect_status']}，实际{resp.status_code}"

        allure.attach(str(preferences_dict), "请求的偏好设置字典", allure.attachment_type.TEXT)


# ------------------------------------------------
# 个人中心-安全与会话管理
# ------------------------------------------------
@allure.feature("个人信息管理")
class TestSecurity:
    @allure.story("活动会话管理")
    @pytest.mark.parametrize("case", get_security_cases(), ids=lambda x: x["case_name"])
    def test_security_actions(self, login_client, case):
        api, current_uid = login_client

        if case.get("action") == "revoke_all":
            with allure.step(f"执行：{case['case_name']}"):
                resp = api.revoke_all_other_sessions()
        else:
            token_id = case["token_id"]
            with allure.step(f"执行：{case['case_name']}"):
                resp = api.revoke_access_token(token_id)

        with allure.step("校验接口响应状态码"):
            assert resp.status_code == case[
                "expect_status"], f"预期状态码{case['expect_status']}，实际{resp.status_code}"

        allure.attach(f"响应状态码: {resp.status_code}", "接口请求与返回信息", allure.attachment_type.TEXT)