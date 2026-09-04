import yaml
from pathlib import Path

def read_yaml(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if data is not None else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML文件不存在：{file_path}")
    except Exception as e:
        raise Exception(f"解析YAML失败：{str(e)}")

def _get_cases(file_name, key):
    root_dir = Path(__file__).parent.parent
    yaml_path = root_dir / "data" / file_name
    yaml_data = read_yaml(yaml_path)
    return yaml_data.get(key, [])

# 认证模块读取器
def get_login_case():
    return _get_cases("auth_data.yaml", "login_cases")
def get_register_case():
    return _get_cases("auth_data.yaml", "register_cases")
def get_forgot_pwd_case():
    return _get_cases("auth_data.yaml", "forgot_pwd_cases")

# 个人信息模块读取器
def get_user_info_cases():
    return _get_cases("personal_info_data.yaml", "user_info_cases")
def get_user_settings_cases():
    return _get_cases("personal_info_data.yaml", "user_settings_cases")
def get_notification_privacy_cases():
    return _get_cases("personal_info_data.yaml", "notification_privacy_cases")
def get_security_cases():
    return _get_cases("personal_info_data.yaml", "security_cases")

# 帖子模块
def get_post_cases():
    return _get_cases("posts_data.yaml", "post_cases")

# 读取评论模块测试用例
def get_comment_cases():
    return _get_cases("comments_data.yaml", "comment_cases")