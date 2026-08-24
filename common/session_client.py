import requests
import re
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from config.settings import BASE_URL, BASE_HEADERS, REQ_TIMEOUT

# 关闭不安全SSL警告（仅测试环境使用）
urllib3.disable_warnings(InsecureRequestWarning)

class SessionClient:
    def __init__(self):
        self.session = requests.Session()                       # 持久会话对象，会自动管理 Cookie
        self.base_url = BASE_URL
        self.session.headers.update(BASE_HEADERS)

    def get_new_csrf_token(self):
        """
        获取最新的 CSRF 令牌
        Flarum 的 CSRF Token 保存在登录页面的 HTML 源代码的 JS 配置段中
        这个 Token 是一次的，每次 GET 首页都会更新，旧 Token 立即失效
        所以每次 POST、PATCH 等写操作前，必须重新提取一次
        """
        try:
            # verify=False 表示跳过 SSL 证书校验，适合在本地开发测试环境使用
            resp = self.session.get(self.base_url, timeout=REQ_TIMEOUT, verify=False)
        except Exception as e:
            # 捕获底层的网络异常，将原生异常包装成具有业务含义的异常抛出，便于排查是网络问题还是代码问题
            raise Exception(f"访问首页获取CSRF页面失败：{str(e)}")

        # 使用正则提取隐藏的 csrfToken，执行速度比解析 HTML DOM 快，且不依赖第三方 HTML 解析库
        token_pattern = r'"csrfToken":"([0-9a-zA-Z]+)"'
        match_res = re.search(token_pattern, resp.text)
        if not match_res:
            raise Exception("页面中未匹配到csrfToken，无法执行提交操作")
        return match_res.group(1)           # group(1) 表示获取正则表达式中第一个括号捕获的纯 Token 字符串

    def _base_request(self, method, path, params=None, json_data=None):
        full_url = f"{self.base_url}{path}"

        temp_headers = {}
        if method.upper() != "GET":     # 只有 GET 请求不需要 CSRF Token，其他所有写操作（增删改）都必须携带 Token
            token = self.get_new_csrf_token()
            temp_headers["X-CSRF-Token"] = token

        # 使用 self.session.request，保证 Cookie 自动传递和关联
        resp = self.session.request(
            method=method,
            url=full_url,
            params=params,
            json=json_data,
            headers=temp_headers,
            timeout=REQ_TIMEOUT,
            verify=False
        )
        return resp

    # HTTP 方法封装
    def get(self, path, params=None):
        return self._base_request("GET", path, params=params)

    def post(self, path, json_data):
        return self._base_request("POST", path, json_data=json_data)

    def patch(self, path, json_data):
        return self._base_request("PATCH", path, json_data=json_data)

    def delete(self, path, json_data=None):
        return self._base_request("DELETE", path, json_data=json_data)

    # 专门用于上传文件（multipart/form-data）的请求方法
    def post_files(self, path, files=None, data=None, headers=None):
        """专门用于上传文件（multipart/form-data）的请求方法"""
        full_url = f"{self.base_url}{path}"

        # 如果外部传入了特定的 headers（如 Referer/Origin），需要合并进去，不能覆盖原有的 Token
        if headers:
            temp_headers = {**self.session.headers, **headers}
        else:
            temp_headers = self.session.headers

        resp = self.session.request(
            method="POST",
            url=full_url,
            files=files,
            data=data,
            headers=temp_headers,
            timeout=REQ_TIMEOUT,
            verify=False
        )
        return resp