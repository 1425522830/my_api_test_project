import requests
import re
import time
import logging
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from config.settings import BASE_URL, BASE_HEADERS, REQ_TIMEOUT, VERIFY_SSL

urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SessionClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.session.headers.update(BASE_HEADERS)

    def get_new_csrf_token(self):
        try:
            resp = self.session.get(self.base_url, timeout=REQ_TIMEOUT, verify=VERIFY_SSL)
        except Exception as e:
            raise Exception(f"访问首页获取CSRF页面失败：{str(e)}")

        token_pattern = r'"csrfToken":"([0-9a-zA-Z]+)"'
        match_res = re.search(token_pattern, resp.text)
        if not match_res:
            raise Exception("页面中未匹配到csrfToken，无法执行提交操作")
        return match_res.group(1)

    def _base_request(self, method, path, params=None, json_data=None):
        full_url = f"{self.base_url}{path}"
        logger.info(f"发起请求: {method} {full_url}")

        temp_headers = {}
        if method.upper() != "GET":
            token = self.get_new_csrf_token()
            temp_headers["X-CSRF-Token"] = token

        resp = self.session.request(
            method=method, url=full_url, params=params, json=json_data,
            headers=temp_headers, timeout=REQ_TIMEOUT, verify=VERIFY_SSL
        )

        retry_count = 0
        while resp.status_code == 429 and retry_count < 2:
            logger.warning("触发429限流，等待10秒后重试...")
            time.sleep(10)
            resp = self.session.request(
                method=method, url=full_url, params=params, json=json_data,
                headers=temp_headers, timeout=REQ_TIMEOUT, verify=VERIFY_SSL
            )
            retry_count += 1

        logger.info(f"响应状态: {resp.status_code} | 耗时: {resp.elapsed.total_seconds()}秒")
        return resp

    def get(self, path, params=None):
        return self._base_request("GET", path, params=params)

    def post(self, path, json_data):
        return self._base_request("POST", path, json_data=json_data)

    def patch(self, path, json_data):
        return self._base_request("PATCH", path, json_data=json_data)

    def delete(self, path, json_data=None):
        return self._base_request("DELETE", path, json_data=json_data)

    def post_files(self, path, files=None, data=None, headers=None):
        full_url = f"{self.base_url}{path}"
        if headers:
            temp_headers = {**self.session.headers, **headers}
        else:
            temp_headers = self.session.headers

        resp = self.session.request(
            method="POST", url=full_url, files=files, data=data,
            headers=temp_headers, timeout=REQ_TIMEOUT, verify=VERIFY_SSL
        )
        return resp