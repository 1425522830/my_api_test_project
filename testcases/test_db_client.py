# 数据库访问层测试：验证 DBClient 的 CRUD、事务回滚、异常处理
# 注意：由于被测 API 无注册接口，本测试不模拟业务，仅测试数据库访问层能力

import allure
import pytest
import os
from common.db_util import DBClient
from common.yaml_util import read_yaml

def get_db_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, 'data', 'db_data.yaml')
    data = read_yaml(yaml_path)
    if not isinstance(data, dict):
        return []
    return data.get('db_tests', [])

@allure.feature("数据库访问层测试")
class TestDatabaseAccessLayer:

    @allure.story("验证 DBClient 的 CRUD 和事务回滚")
    @pytest.mark.parametrize("case", get_db_cases(), ids=lambda x: x['name'])
    def test_db_client_operations(self, case, db_client):
        username = case.get('username')
        email = case.get('email')
        expect_success = case.get('expect_success', True)
        check_rollback = case.get('check_rollback', False)

        # 1. 物理删除可能残留的同名数据（确保干净环境）
        db_client.execute("DELETE FROM users WHERE username = %s", (username,))
        db_client.commit()

        # 2. 开启事务
        db_client.begin()
        try:
            if expect_success:
                with allure.step(f"插入数据: username={username}, email={email}"):
                    db_client.execute(
                        "INSERT INTO users (username, email) VALUES (%s, %s)",
                        (username, email)
                    )

                with allure.step("查询验证数据是否存在"):
                    result = db_client.fetch_one(
                        "SELECT COUNT(*) FROM users WHERE username = %s", (username,)
                    )
                    count = result[0] if result else 0
                    assert count == 1, f"插入后查询到 {count} 条记录，预期 1 条"

                if check_rollback:
                    with allure.step("验证回滚后数据不存在"):
                        db_client.rollback()
                        db_client.begin()   # 回滚后重新开启事务（其实可以直接查询，但为了演示）
                        result = db_client.fetch_one(
                            "SELECT COUNT(*) FROM users WHERE username = %s", (username,)
                        )
                        count = result[0] if result else 0
                        assert count == 0, f"回滚后仍存在 {count} 条记录，预期 0 条"
                else:
                    # 不检查回滚，则最终回滚事务（保证用例隔离，不提交数据）
                    db_client.rollback()
            else:
                # 预期失败的情况（本例无，但保留扩展）
                pytest.fail("Unexpected failure case")
        except Exception as e:
            db_client.rollback()
            raise e

    @allure.story("测试唯一约束（重复插入）")
    def test_duplicate_insert(self, db_client):
        """单独测试重复插入唯一约束，避免数据驱动依赖问题"""
        username = "dup_test_user"
        email_first = "dup1@example.com"
        email_second = "dup2@example.com"

        # 清理可能的历史数据
        db_client.execute("DELETE FROM users WHERE username = %s", (username,))
        db_client.commit()

        # 第一次插入（提交，使数据持久化）
        db_client.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            (username, email_first)
        )
        db_client.commit()

        # 第二次插入相同用户名，应违反唯一约束
        with pytest.raises(Exception) as exc_info:
            db_client.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (username, email_second)
            )
        assert "duplicate" in str(exc_info.value).lower(), f"错误信息不包含 'duplicate': {exc_info.value}"

        # 清理测试数据
        db_client.execute("DELETE FROM users WHERE username = %s", (username,))
        db_client.commit()