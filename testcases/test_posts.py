import allure
import pytest
from api.post_api import PostApi
from common.yaml_util import get_post_cases

@allure.feature("帖子模块")
class TestPostManagement:
    @allure.story("帖子模块-数据驱动测试")
    @pytest.mark.parametrize("case", get_post_cases(), ids=lambda x: x["case_name"])
    def test_post_data_driven(self, login_client, raw_client, login_client_b, case):
        if case.get("operate") == "create":
            api, _ = login_client
            post_api = PostApi(api.client)
            tag_id = post_api.get_primary_tag_id()
            resp = post_api.create_discussion(case["title"], case["content"], tag_ids=[tag_id])
        elif case.get("operate") == "create_unauth":
            post_api = PostApi(raw_client)
            resp = post_api.create_discussion(case["title"], case["content"])
        elif case.get("operate") == "create_no_tag":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.create_discussion(case["title"], case["content"])
        elif case.get("operate") == "list":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.get_discussions_list(page_offset=case["page_offset"], sort=case["sort"])
        elif case.get("operate") == "detail_not_found":
            api, _ = login_client
            post_api = PostApi(api.client)
            resp = post_api.get_discussion_detail(case["discussion_id"])
        elif case.get("operate") == "cross_user_edit":
            if not login_client_b:
                pytest.skip("未配置账号B，跳过越权测试")
            api_a, _ = login_client
            api_b, _ = login_client_b
            post_api_a = PostApi(api_a.client)
            post_api_b = PostApi(api_b.client)
            tag_id = post_api_a.get_primary_tag_id()
            resp = post_api_a.create_discussion("越权测试", "内容", tag_ids=[tag_id])
            assert resp.status_code == 201
            data_id = resp.json()["data"]["id"]
            post_id = post_api_a.get_first_post_id(data_id)
            resp = post_api_b.edit_post(post_id, content="篡改成功")
        else:
            pytest.skip(f"未实现的操作: {case.get('operate')}")

        assert resp.status_code == case["expect_status"], f"预期{case['expect_status']}，实际{resp.status_code}"
        if resp.status_code in [200, 201]:
            assert "data" in resp.json()

    @allure.story("帖子模块-完整生命周期闭环")
    def test_full_lifecycle(self, new_discussion):
        post_api = new_discussion["post_api"]
        discussion_id = new_discussion["created_id"]
        first_post_id = new_discussion["first_post_id"]
        with allure.step("查看详情"):
            assert post_api.get_discussion_detail(discussion_id).status_code == 200
        with allure.step("编辑帖子"):
            assert post_api.edit_post(first_post_id, content="修改后的内容").status_code == 200
        with allure.step("删除帖子"):
            assert post_api.delete_discussion(discussion_id).status_code == 200

    @allure.story("帖子模块-数据一致性(防假成功)")
    def test_delete_then_check_detail(self, new_discussion):
        post_api = new_discussion["post_api"]
        discussion_id = new_discussion["created_id"]
        assert post_api.delete_discussion(discussion_id).status_code == 200, "删除失败"
        check_resp = post_api.get_discussion_detail(discussion_id)
        assert check_resp.status_code == 200, "软删除的帖子详情接口不应该返回403"
        assert check_resp.json()["data"]["attributes"]["isHidden"] is True, "删除后居然还能查到详情且isHidden为False，存在假成功或脏数据！"