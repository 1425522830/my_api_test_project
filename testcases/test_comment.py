import allure
import pytest
from api.comment_api import CommentApi
from common.yaml_util import get_comment_cases


@allure.feature("评论模块")
class TestComments:
    @allure.story("评论生命周期闭环测试")
    def test_comment_lifecycle(self, new_discussion):
        post_api = new_discussion["post_api"]
        discussion_id = new_discussion["created_id"]
        comment_api = CommentApi(post_api.client)

        resp = comment_api.create_post(discussion_id, "你好，测试")
        assert resp.status_code == 201
        first_comment_id = resp.json()["data"]["id"]

        resp = comment_api.create_post(discussion_id, f"@湖笙 #{first_comment_id} 对的，对的")
        assert resp.status_code == 201

        assert comment_api.delete_post(first_comment_id).status_code == 200

    @allure.story("评论模块-数据驱动异常测试")
    @pytest.mark.parametrize("case", get_comment_cases(), ids=lambda x: x["case_name"])
    def test_comment_data_driven(self, new_discussion, case):
        discussion_id = new_discussion["created_id"]
        comment_api = CommentApi(new_discussion["post_api"].client)
        resp = comment_api.create_post(discussion_id, case["content"])
        assert resp.status_code == case["expect_status"]

    @allure.story("评论模块-越权测试")
    def test_cross_user_delete_comment(self, new_discussion, login_client_b):
        if not login_client_b:
            pytest.skip("未配置账号B，跳过越权测试")

        post_api = new_discussion["post_api"]
        discussion_id = new_discussion["created_id"]
        comment_api = CommentApi(post_api.client)

        resp = comment_api.create_post(discussion_id, "这是一条A的评论")
        assert resp.status_code == 201
        comment_id = resp.json()["data"]["id"]

        b_comment_api = CommentApi(login_client_b[0].client)
        del_resp = b_comment_api.delete_post(comment_id)

        assert del_resp.status_code in [403, 404], f"越权删除竟成功了，请检查权限漏洞！实际返回{del_resp.status_code}"