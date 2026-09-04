# 论坛项目全局配置

BASE_URL = "https://www.wangdanatest.top"           # 站点根域名，作为所有接口请求的前缀

# 测试账号
TEST_ACCOUNT = "1425522830@qq.com"                  # 自动化测试专用的预注册账号
TEST_PWD = "6666666666"                             # 对应的密码

# 请求基础头
BASE_HEADERS = {
    "Content-Type": "application/json; charset=utf-8"       # 指定请求体的格式为 JSON，适配 Flarum 标准接口
}

# 请求超时秒数
REQ_TIMEOUT = 10                                    # 网络请求最长等待时间。防止由于网络故障导致用例长时间挂起

# 接口路径常量
API_LOGIN = "/login"                                # 登录接口
API_REGISTER = "/register"                          # 注册接口
API_FORGOT = "/api/forgot"                          # 忘记密码
API_USERS = "/api/users"                            # 用户信息管理接口（更新昵称/简介）
API_ACCESS_TOKENS = "/api/access-tokens"            # 活动会话（访问令牌）管理接口
API_SESSIONS = "/api/sessions"                      # 会话管理接口（终止所有其他会话）
API_AVATAR = "/avatar"                              # 头像上传路径

API_POSTS = "/api/posts"                            # 帖子/回复相关接口
API_DISCUSSIONS = "/api/discussions"                # 主题讨论相关接口

