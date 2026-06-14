#  商品模块的只读接口（列表查询、关键词搜索、分页）

#  商品模块的只读接口（列表查询、关键词搜索、分页）


# 商品模块的只读接口测试（数据驱动，全部从 YAML 加载）

import allure
import pytest
import os
from common.session_client import SessionClient
from common.yaml_util import read_yaml
from config.settings import BASE_URL

def get_product_cases():
    """
    从 YAML 加载所有商品测试用例，并返回 (case_type, case) 列表。
    包含完整的错误检查，自动定位非字典条目。
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, 'data', 'products_data.yaml')
    data = read_yaml(yaml_path)

    # 错误检查：打印解析结果并定位问题
    if not isinstance(data, dict):
        print(f"ERROR: YAML 解析失败，期望 dict，实际得到 {type(data)}")
        return []

    cases = []

    # 定义需要检查的列表键名
    list_keys = {
        'product_list_tests': 'list',
        'search_tests': 'search',
        'category_tests': 'category',   # 内部会再区分 endpoint
        'product_detail_tests': 'detail'
    }

    for key, case_type_base in list_keys.items():
        items = data.get(key, [])
        if not isinstance(items, list):
            print(f"ERROR: {key} 不是列表，而是 {type(items)}，跳过")
            continue
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                print(f"ERROR: {key}[{idx}] 不是字典，而是 {type(item)}，值为：{item}")
                print(f"   请检查 YAML 中该行是否正确（是否缺少冒号/缩进/引号）")
                continue
            # 根据 key 决定最终 case_type
            if key == 'category_tests':
                # 分类测试有两种类型
                if 'endpoint' in item:
                    cases.append(('category_list', item))
                else:
                    cases.append(('category_products', item))
            else:
                cases.append((case_type_base, item))

    print(f"[INFO] 共加载 {len(cases)} 条商品测试用例")
    return cases


def safe_id_func(val):
    """安全的 ids 函数，处理各种可能的参数类型"""
    try:
        if isinstance(val, (tuple, list)) and len(val) >= 2 and isinstance(val[1], dict):
            return val[1].get('name', 'unknown')
        else:
            return str(val)
    except Exception:
        return "invalid_case"


@allure.feature("商品模块")
class TestProductsDataDriven:
    @allure.story("商品接口数据驱动测试")
    @pytest.mark.parametrize("case_type, case", get_product_cases(), ids=safe_id_func)
    def test_products_ddt(self, case_type, case):
        client = SessionClient(base_url=BASE_URL)
        with allure.step(f"执行用例：{case['name']}"):
            # 商品列表测试
            if case_type == 'list':
                params = case.get('params', {})
                resp = client.get("/products", params=params)
                assert resp.status_code == case['expected_status']
                if case.get('expect_products'):
                    assert 'products' in resp.json()
                if case.get('max_items') is not None:
                    assert len(resp.json()['products']) <= case['max_items']
                if case.get('exact_items') is not None:
                    assert len(resp.json()['products']) == case['exact_items']
                if case.get('expect_products_empty'):
                    assert len(resp.json()['products']) == 0

            # 商品搜索测试
            elif case_type == 'search':
                keyword = case['keyword']
                resp = client.get("/products/search", params={'q': keyword})
                assert resp.status_code == case['expected_status']
                if case.get('expect_any_match'):
                    products = resp.json()['products']
                    assert any(keyword.lower() in p['title'].lower() for p in products)
                if case.get('expect_products_empty'):
                    assert len(resp.json()['products']) == 0

            # 分类列表测试
            elif case_type == 'category_list':
                resp = client.get(case['endpoint'])
                assert resp.status_code == case['expected_status']
                if case.get('expect_list'):
                    categories = resp.json()
                    assert isinstance(categories, list)
                    assert len(categories) >= case.get('min_items', 1)

            # 指定分类下的商品测试
            elif case_type == 'category_products':
                category = case['category']
                resp = client.get(f"/products/category/{category}")
                assert resp.status_code == case['expected_status']
                if case.get('validate_category'):
                    products = resp.json()['products']
                    assert len(products) > 0
                    for p in products:
                        assert p['category'].lower() == category.lower()

            # 商品详情测试
            elif case_type == 'detail':
                product_id = case['product_id']
                resp = client.get(f"/products/{product_id}")
                assert resp.status_code == case['expected_status']
                if case.get('check_fields'):
                    data = resp.json()
                    for field in case['check_fields']:
                        assert field in data