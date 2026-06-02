#  测试需要登录的接口，编写需鉴权的接口测试（用户信息、购物车查询）验证接口关联问题

from config.settings import LOGIN_USERNAME

def test_get_user_info(api_client):
    # 测试获取当前用户信息
    resp = api_client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.json()["username"] == LOGIN_USERNAME

def test_get_cart(api_client):
    # 测试购物车查询
    me = api_client.get("/auth/me")
    assert me.status_code == 200
    user_id = me.json()["id"]
    resp = api_client.get(f"/carts/user/{user_id}")
    assert resp.status_code == 200
    assert "carts" in resp.json()