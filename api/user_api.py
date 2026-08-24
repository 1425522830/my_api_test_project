from config.settings import API_LOGIN, API_REGISTER, API_FORGOT, API_POSTS, API_DISCUSSIONS, API_FOF_UPLOADS, \
    REQ_TIMEOUT, API_USERS, API_ACCESS_TOKENS, API_SESSIONS, API_AVATAR

# 用户模块接口封装
class UserApi:
    def __init__(self, client):
        self.client = client        # 组合注入HTTP会话客户端，解耦优于继承

    # 登录接口
    def login(self, identification, password, remember=False):
        req_body = {
            "identification": identification,
            "password": password,
            "remember": remember
        }

        token = self.client.get_new_csrf_token()            # 获取一次性的游客 token
        full_url = f"{self.client.base_url}{API_LOGIN}"
        headers = {**self.client.session.headers, "X-CSRF-Token": token}

        # Flarum 登录时必须使用“游客身份”且携带刚生成的 Token 进行提交。
        # 这里使用原生 request，绕开了底层 `post` 自带的_极可能触发二次 GET 页面的逻辑。
        return self.client.session.request(
            "POST", full_url, json=req_body, headers=headers, timeout=REQ_TIMEOUT, verify=False
        )

    # 注册接口
    def register(self, email, nickname, password, username):
        req_body = {
            "email": email,
            "nickname": nickname,
            "password": password,
            "username": username
        }
        resp = self.client.post(path=API_REGISTER, json_data=req_body)
        return resp

    # 忘记密码
    def send_forgot_pwd_email(self, email: str):
        req_body = {
            "email": email
        }
        resp = self.client.post(path=API_FORGOT, json_data=req_body)
        return resp
    
    # 更改个人资料（昵称、简介等）
    def update_user_profile(self, user_id: int, nickname: str = None, bio: str = None):
        req_body = {
            "data": {
                "type": "users",
                "id": str(user_id),
                "attributes": {}
            }
        }
        if nickname is not None:
            req_body["data"]["attributes"]["nickname"] = nickname
        if bio is not None:
            req_body["data"]["attributes"]["bio"] = bio

        return self.client.patch(path=f"{API_USERS}/{user_id}", json_data=req_body)

    # 更新用户偏好设置（通知、隐私等）支持部分更新
    def update_user_preferences(self, user_id: int, preferences: dict):     # preferences 是一个字典
        req_body = {
            "data": {
                "type": "users",
                "id": str(user_id),
                "attributes": {
                    "preferences": preferences
                }
            }
        }
        # Flarum 标准更新属性接口，必须用 PATCH
        return self.client.patch(path=f"{API_USERS}/{user_id}", json_data=req_body)

    # 终止会话
    def revoke_access_token(self, token_id: int):
        return self.client.delete(path=f"{API_ACCESS_TOKENS}/{token_id}")

    # 终止所有其他会话（安全设置内的批量退出）
    def revoke_all_other_sessions(self):
        # 请求体为空 {}，因为是批量撤销，不需要传指定的 ID
        return self.client.delete(path=API_SESSIONS, json_data={})

