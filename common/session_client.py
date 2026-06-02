# 会话客户端，封装requests.Session实现会话保持、公共请求头注入及HTTP方法封装

import requests
from config.settings import HEADERS, REQUEST_TIMEOUT

class SessionClient:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.update_headers(HEADERS)

    def _build_url(self, endpoint):
        if self.base_url:
            return f"{self.base_url}{endpoint}"
        return endpoint

    def post(self, endpoint, timeout=REQUEST_TIMEOUT, **kwargs):
        url = self._build_url(endpoint)
        return self.session.post(url, timeout=timeout, **kwargs)

    def get(self, endpoint, timeout=REQUEST_TIMEOUT, **kwargs):
        url = self._build_url(endpoint)
        return self.session.get(url, timeout=timeout, **kwargs)

    def set_header(self, key, value):
        self.session.headers[key] = value

    def update_headers(self, headers):
        self.session.headers.update(headers)




