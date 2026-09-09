import mimetypes
from config.settings import (API_LOGIN, API_REGISTER, API_FORGOT, REQ_TIMEOUT,
                             API_USERS, API_ACCESS_TOKENS, API_SESSIONS, API_AVATAR, VERIFY_SSL)

class UserApi:
    def __init__(self, client):
        self.client = client

    def login(self, identification, password, remember=False):
        req_body = {"identification": identification, "password": password, "remember": remember}
        return self.client.post(path=API_LOGIN, json_data=req_body)

    def register(self, email, nickname, password, username):
        req_body = {"email": email, "nickname": nickname, "password": password, "username": username}
        return self.client.post(path=API_REGISTER, json_data=req_body)

    def send_forgot_pwd_email(self, email: str):
        return self.client.post(path=API_FORGOT, json_data={"email": email})

    def update_user_profile(self, user_id: int, nickname: str = None, bio: str = None):
        req_body = {"data": {"type": "users", "id": str(user_id), "attributes": {}}}
        if nickname is not None: req_body["data"]["attributes"]["nickname"] = nickname
        if bio is not None: req_body["data"]["attributes"]["bio"] = bio
        return self.client.patch(path=f"{API_USERS}/{user_id}", json_data=req_body)

    def update_user_preferences(self, user_id: int, preferences: dict):
        req_body = {"data": {"type": "users", "id": str(user_id), "attributes": {"preferences": preferences}}}
        return self.client.patch(path=f"{API_USERS}/{user_id}", json_data=req_body)

    def get_user_access_tokens(self, user_id: int):
        return self.client.get(path=f"{API_USERS}/{user_id}/access-tokens")

    def revoke_access_token(self, token_id: int):
        return self.client.delete(path=f"{API_ACCESS_TOKENS}/{token_id}")

    def revoke_all_other_sessions(self):
        return self.client.delete(path=API_SESSIONS, json_data={})

    def upload_avatar(self, user_id: int, file_path: str):
        full_path = f"{API_USERS}/{user_id}{API_AVATAR}"
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None: content_type = 'application/octet-stream'
        with open(file_path, 'rb') as f:
            files = {'avatar': (file_path.split('/')[-1], f, content_type)}
            headers = {
                "X-CSRF-Token": self.client.get_new_csrf_token(),
                "Referer": f"{self.client.base_url}/settings",
                "Origin": self.client.base_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36"
            }
            return self.client.post_files(path=full_path, files=files, headers=headers)

    def remove_avatar(self, user_id: int):
        full_url = f"{self.client.base_url}{API_USERS}/{user_id}{API_AVATAR}"
        token = self.client.get_new_csrf_token()
        headers = {
            "X-CSRF-Token": token,
            "Referer": f"{self.client.base_url}/settings",
            "Origin": self.client.base_url
        }
        return self.client.session.request("POST", full_url, headers=headers, timeout=REQ_TIMEOUT, verify=VERIFY_SSL)