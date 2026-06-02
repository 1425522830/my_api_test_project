# 接口自动化测试框架（Python + Pytest + Allure）

## 

##### 项目简介

&#x09;本项目是一个基于 **Python + Pytest + Requests + Allure** 构建的接口自动化测试框架，针对 DummyJSON 提供的开放 API 进行测试。实现了**登录鉴权（Token）**、**接口依赖**、**数据驱动**、**Allure 报告**、**数据库校验**等测试框架的核心功能。



##### 技术栈

|工具/库|用途|
|-|-|
|Python 3.13|编程语言|
|Requests|发送 HTTP 请求|
|Pytest|测试框架，管理用例、断言|
|Allure|生成可视化测试报告|
|PyYAML|读取 YAML 格式的测试数据|
|PyMySQL|连接 MySQL 进行数据校验|
|Git|版本控制|



##### 快速开始

###### &#x09;1. 克隆项目  

&#x20;  `	 	git clone https://github.com/1425522830/my\_api\_test\_project.git`



###### &#x09;2. 安装依赖  

&#x20;  		`pip install -r requirements.txt`



###### &#x09;3. 配置数据库（可选）  

&#x20; 		 修改 `config/settings.py` 中的数据库连接信息，并在 MySQL 中手动创建 `users` 表。



###### &#x09;4. 运行测试  

&#x20;  		`python run\_tests.py`



###### &#x09;5. 查看 Allure 报告  

&#x20;  		运行后会自动打开浏览器展示报告。

