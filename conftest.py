import pytest
from common.session_client import SessionClient
from api.user_api import UserApi
from api.post_api import PostApi
from config.settings import TEST_ACCOUNT, TEST_PWD, TEST_ACCOUNT_B, TEST_PWD_B

# 无需接口关联，用于登录相关用例
@pytest.fixture(scope="function")
def raw_client():
    c = SessionClient()
    yield c

# 用于需要接口关联的登录后的有关用例，获得 用户id 便于后续用户相关操作
@pytest.fixture(scope="session")
def login_client():
    c = SessionClient()
    api = UserApi(c)
    login_resp = api.login(TEST_ACCOUNT, TEST_PWD)
    assert login_resp.status_code == 200, f"登录失败：{login_resp.text}"
    resp_json = login_resp.json()
    if "errors" in resp_json:
        assert False, f"登录接口隐藏报错：{resp_json['errors']}"
    if "userId" not in resp_json:
        raise AssertionError(f"登录响应成功但缺少 'userId' 字段！请检查：{resp_json}")
    uid = resp_json["userId"]
    yield (api, uid)

# 配置B账号测试越权，未配置则跳过
@pytest.fixture(scope="session")
def login_client_b():
    if not TEST_ACCOUNT_B or not TEST_PWD_B:
        pytest.skip("未配置测试账号B，跳过越权测试")
    c = SessionClient()
    api = UserApi(c)
    login_resp = api.login(TEST_ACCOUNT_B, TEST_PWD_B)
    if login_resp.status_code != 200:
        pytest.skip("测试账号B登录失败，跳过越权测试")
    yield (api, login_resp.json()["userId"])

# 创建帖子 —— 用于评论功能用例测试，须有一个帖子作为前置条件，便于数据闭环与自动清理，不写在帖子相关测试用例
@pytest.fixture(scope="function")
def new_discussion(login_client):
    api, current_uid = login_client
    post_api = PostApi(api.client)
    tag_id = post_api.get_primary_tag_id()
    created_id = None
    first_post_id = None

    if not tag_id:
        pytest.skip("未获取到主分类Tag，无法创建帖子")
        yield None
        return

    resp = post_api.create_discussion("动态夹具帖", "自动生成", tag_ids=[tag_id])
    if resp.status_code == 201:
        created_id = resp.json()["data"]["id"]
        first_post_id = post_api.get_first_post_id(created_id)

    yield {"post_api": post_api, "created_id": created_id, "first_post_id": first_post_id}

    if created_id:
        try:
            post_api.delete_discussion(created_id)
        except Exception:
            pass