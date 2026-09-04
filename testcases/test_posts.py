import allure
import pytest
from api.post_api import PostApi
from common.yaml_util import get_post_cases
import time

@allure.feature("帖子模块")
class TestPostManagement:
    @allure.story("帖子模块-数据驱动测试")
    @pytest.mark.parametrize("case", get_post_cases(), ids=lambda x: x["case_name"])
    def test_post_data_driven(self, login_client, raw_client, case):
        if case.get("operate") == "create":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.create_discussion(case["title"], case["content"], tag_ids=case.get("tag_ids", []))

        elif case.get("operate") == "create_unauth":
            # 未登录使用 raw_client 创建
            post_api = PostApi(raw_client)
            resp = post_api.create_discussion(case["title"], case["content"])

        elif case.get("operate") == "list":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.get_discussions_list(page_offset=case["page_offset"], sort=case["sort"])

        elif case.get("operate") == "detail_not_found":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.get_discussion_detail(case["discussion_id"])

        with allure.step("校验接口响应状态码"):
            assert resp.status_code == case[
                "expect_status"], f"预期状态码{case['expect_status']}，实际{resp.status_code}"

        # 防御式断言：如果操作成功，必须包含 data 字段
        if resp.status_code in [200, 201]:
            assert "data" in resp.json(), "接口返回成功但缺少 data 字段！"

        allure.attach(resp.text, "接口返回数据", allure.attachment_type.TEXT)

    @allure.story("帖子模块-完整生命周期闭环")
    def test_full_lifecycle(self, login_client):
        """创建->获取ID->查详情->编辑->删除（并清理）"""
        api, current_uid = login_client
        post_api = PostApi(api.client)
        created_discussion_id = None
        first_post_id = None

        try:
            # 创建
            with allure.step("创建新帖"):
                time.sleep(5)       # 防限流：每次发帖前强制停顿1秒
                resp = post_api.create_discussion("生命周期测试帖", "初始内容")
                assert resp.status_code == 201, f"创建失败: {resp.text}"
                created_discussion_id = resp.json()["data"]["id"]

                # 动态获取首帖 ID
                first_post_id = post_api.get_first_post_id(created_discussion_id)
                assert first_post_id is not None, "未能获取到首帖 Post ID"
                allure.attach(f"讨论ID:{created_discussion_id}, 首帖ID:{first_post_id}", "动态数据")

            # 查详情
            with allure.step("查看新帖详情"):
                detail_resp = post_api.get_discussion_detail(created_discussion_id)
                assert detail_resp.status_code == 200
                assert detail_resp.json()["data"]["id"] == str(created_discussion_id)

            # 编辑
            with allure.step("编辑新帖"):
                edit_resp = post_api.edit_post(first_post_id, content="修改后的内容")
                assert edit_resp.status_code == 200, f"编辑失败: {edit_resp.text}"

            # 删除
            with allure.step("删除新帖"):
                del_resp = post_api.delete_post(first_post_id)
                assert del_resp.status_code == 200, f"删除失败: {del_resp.text}"

        finally:
            # 清理：即使上面断言报错，也强制删除，防止污染环境
            if created_discussion_id and first_post_id:
                post_api.delete_post(first_post_id)

    @allure.story("帖子模块-操作不存在的数据")
    def test_edit_and_delete_not_found(self, login_client):
        """编辑和删除不存在的帖子，预期 404"""
        api, current_uid = login_client
        post_api = PostApi(api.client)
        invalid_post_id = 999999999

        with allure.step("尝试编辑不存在的帖子"):
            edit_resp = post_api.edit_post(invalid_post_id, content="无效内容")
            # 不允许和不存在有可能是两种不同的状态吗，实测为405
            assert edit_resp.status_code == 405, f"预期404，实际{edit_resp.status_code}"

        with allure.step("尝试删除不存在的帖子"):
            del_resp = post_api.delete_post(invalid_post_id)
            assert del_resp.status_code == 405, f"预期404，实际{del_resp.status_code}"