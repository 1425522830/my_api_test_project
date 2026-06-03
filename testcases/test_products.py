#  商品模块的只读接口（列表查询、关键词搜索、分页）

import allure
import pytest
from common.session_client import SessionClient
from config.settings import BASE_URL
# testcases/test_products.py
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
        assert any(keyword.lower() in p["title"].lower() for p in products), \
            f"搜索 {keyword} 没有匹配标题的商品"

    @allure.story("商品分页查询")
    def test_products_pagination(self):
        resp = self.client.get("/products", params={"limit": 5, "skip": 5})
        assert resp.status_code == 200
        products = resp.json()["products"]
        assert len(products) == 5

    @allure.story("获取商品分类列表")
    def test_get_categories(self):
        resp = self.client.get("/products/categories")
        assert resp.status_code == 200
        categories = resp.json()
        assert isinstance(categories, list)
        assert len(categories) > 0
        for cat in categories:
            assert isinstance(cat, dict)
            assert 'name' in cat
            assert cat['name']  # 非空字符串

    @allure.story("获取指定分类下的商品")
    def test_get_products_by_category(self):
        category = "smartphones"
        resp = self.client.get(f"/products/category/{category}")
        assert resp.status_code == 200
        products = resp.json()["products"]
        assert len(products) > 0
        for p in products:
            assert p["category"].lower() == category

    @allure.story("获取单个商品详情")
    def test_get_single_product(self):
        product_id = 1
        resp = self.client.get(f"/products/{product_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == product_id
        assert "title" in data
        assert "price" in data