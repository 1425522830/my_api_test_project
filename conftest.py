import pytest
from common.session_client import SessionClient
from api.user_api import UserApi
from config.settings import TEST_ACCOUNT, TEST_PWD

# 不需要登录的查询接口（用于注册、未登录异常测等）
@pytest.fixture(scope="function")
def raw_client():
    c = SessionClient()
    yield c

# 需要登录态的业务接口（用于个人信息、已登录操作等）
@pytest.fixture(scope="session")
def login_client():
    c = SessionClient()
    api = UserApi(c)
    login_resp = api.login(TEST_ACCOUNT, TEST_PWD)      # 执行一次登录操作

    # 状态码校验
    assert login_resp.status_code == 200, f"登录失败：状态码异常 {login_resp.status_code}, 内容：{login_resp.text}"

    # 接口实际报错拦截（即便返回 200，也检查有无 errors 字段）
    resp_json = login_resp.json()
    if "errors" in resp_json:
        assert False, f"登录接口隐藏报错：{resp_json['errors']}"

    # 核心数据字段验证
    # 这里直接提取 'userId' 而不是 'data'['id']，这才是此论坛环境的真实返回结构
    if "userId" not in resp_json:
        raise AssertionError(f"登录响应成功但缺少 'userId' 字段！请检查：实际返回的 JSON 是 {resp_json}")
    uid = resp_json["userId"]
    yield (api, uid)            # 直接返回一个元组，不再返回字典
