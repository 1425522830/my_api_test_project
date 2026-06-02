# 模拟数据库状态，演示数据库端到端校验（数据插入、查询断言、清理），验证数据一致性。

import allure

@allure.feature("数据库校验示例")
class TestDatabaseCheck:

    @allure.story("模拟注册用户后查询数据库验证")
    def test_register_db_check(self, db_client):
        # 由于此API没有提供用户注册接口，这里直接通过SQL插入数据来模拟“注册成功后的数据库状态”
        # 目的是验证数据库连接、增删改查及数据清理能力。实际项目中应先调用注册接口，再查询数据库断言落库。
        # 先在MySQL中手动创建users表，
        test_username = "test_user_001"
        test_email = "test@example.com"

        with allure.step("插入测试数据（模拟注册后的数据）"):
            db_client.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (test_username, test_email))

        with allure.step("查询数据库，确认用户已存在"):
            sql = "SELECT COUNT(*) FROM users WHERE username = %s"
            result = db_client.fetch_one(sql, (test_username,))
            count = result[0] if result else 0
            assert count == 1, f"预期用户 {test_username} 存在，实际查询到 {count} 条"

        with allure.step("清理测试数据"):
            db_client.execute("DELETE FROM users WHERE username = %s", (test_username,))