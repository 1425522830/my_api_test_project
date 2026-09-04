import time
import allure
import pytest
from api.comment_api import CommentApi
from api.post_api import PostApi
from common.yaml_util import get_comment_cases


@allure.feature("评论模块")
class TestComments:
    @allure.story("评论生命周期闭环测试")
    def test_comment_lifecycle(self, login_client):
        api, current_uid = login_client
        post_api = PostApi(api.client)
        comment_api = CommentApi(api.client)

        discussion_id = None
        first_post_id = None
        first_comment_id = None

        try:
            # 1. 准备数据：发一个帖子（注意加上防限流）
            time.sleep(5)
            resp = post_api.create_discussion("评论测试帖", "正文", tag_ids=[4, 5])
            assert resp.status_code == 201
            discussion_id = resp.json()["data"]["id"]
            first_post_id = post_api.get_first_post_id(discussion_id)

            # 2. 发一级评论
            with allure.step("发表一级评论"):
                time.sleep(5)
                resp = comment_api.create_post(discussion_id, "你好，测试")
                assert resp.status_code == 201
                first_comment_id = resp.json()["data"]["id"]

            # 3. 发二级评论（回复一级评论，拼上 #楼层ID）
            with allure.step("发表二级评论"):
                time.sleep(5)
                reply_content = f"@湖笙 #{first_comment_id} 对的，对的"
                resp = comment_api.create_post(discussion_id, reply_content)
                assert resp.status_code == 201

            # 4. 删除一级评论（软删除）
            with allure.step("删除评论"):
                time.sleep(5)
                del_resp = comment_api.delete_post(first_comment_id)
                assert del_resp.status_code == 200

        finally:
            # 清理数据：防止测试垃圾数据污染论坛
            if discussion_id and first_post_id:
                time.sleep(5)
                post_api.delete_post(first_post_id)

    @allure.story("评论模块-数据驱动异常测试")
    @pytest.mark.parametrize("case", get_comment_cases(), ids=lambda x: x["case_name"])
    def test_comment_data_driven(self, login_client, case):
        api, current_uid = login_client
        comment_api = CommentApi(api.client)
        # 引用一个必存在的帖子ID 489 作为测试底板
        discussion_id = 489

        with allure.step(f"执行：{case['case_name']}"):
            time.sleep(5)
            resp = comment_api.create_post(discussion_id, case["content"])

        with allure.step("校验响应状态码"):
            assert resp.status_code == case["expect_status"], f"预期{case['expect_status']}，实际{resp.status_code}"