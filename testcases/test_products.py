#  测试商品模块的只读接口（列表查询、关键词搜索、分页）

import allure
import pytest
from common.session_client import SessionClient
from config.settings import BASE_URL

@allure.feature("商品模块")
class TestProducts:

    def setup_method(self):
        self.client = SessionClient(base_url=BASE_URL)

    @allure.story("查询商品列表")
    def test_get_products(self):
        resp = self.client.get("/products", params={"limit": 10})
        assert resp.status_code == 200
        assert "products" in resp.json()
        assert len(resp.json()["products"]) <= 10

    @allure.story("搜索商品")
    @pytest.mark.parametrize("keyword", ["phone", "laptop", "watch"])
    def test_search_products(self, keyword):
        resp = self.client.get("/products/search", params={"q": keyword})
        assert resp.status_code == 200
        products = resp.json()["products"]
        for p in products:
            assert any(keyword.lower() in p["title"].lower() for p in products), \
                f"搜索 {keyword} 没有匹配标题的商品"

    @allure.story("商品分页查询")
    def test_products_pagination(self):
        resp = self.client.get("/products", params={"limit": 5, "skip": 5})
        assert resp.status_code == 200
        products = resp.json()["products"]
        assert len(products) == 5