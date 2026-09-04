# 论坛系统接口自动化测试框架

## 项目简介
基于 Python + Requests + Pytest + Allure 搭建的接口自动化测试框架，覆盖用户、帖子、评论三大核心业务模块，支持数据驱动、动态数据处理和测试环境自愈。

## 技术栈
- Python 3.11
- Requests (HTTP客户端)
- Pytest (测试框架)
- Allure (报告生成)
- YAML (数据驱动)
- python-dotenv (环境变量管理)

## 架构分层
- Config: 全局配置（域名、账号等）
- Common: 底层请求封装、CSRF处理、429限流重试、YAML读取工具
- Api: 各业务模块接口封装
- Testcases: 测试用例
- Data: 测试数据

## 核心难点与解决方案
1. **一次性 CSRF Token处理**：通过每次POST请求前动态解析首页HTML，提取最新Token，解决登录/写操作401问题。
2. **429限流自愈机制**：在底层封装了自动重试逻辑，检测到429后等待10秒自动重试，极大提高了测试稳定性。
3. **动态数据闭环**：通过 `new_discussion` 等 Fixture 实现自动造数、动态提取ID、测试结束自动清理，避免测试数据污染。
4. **安全数据隔离**：密码通过 `.env` 文件注入，不写入Git仓库。

## 运行方式
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `.env` 文件
3. 运行测试：`python run_tests.py`
4. 查看报告：自动生成并打开 Allure 报告