import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()                                       # 必须在文件顶部加载.env，在read_yaml被调用之前执行

def _replace_vars(data):                            # 递归遍历字典/列表，用环境变量替换 ${VAR} 占位符
    if isinstance(data, dict):
        return {k: _replace_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_replace_vars(i) for i in data]
    elif isinstance(data, str):
        return os.path.expandvars(data)
    else:
        return data

# yaml文件读取函数
def read_yaml(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data:
            data = _replace_vars(data)              # 递归替换
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

# yaml文件定位
def _get_cases(file_name, key):
    root_dir = Path(__file__).parent.parent
    yaml_path = root_dir / "data" / file_name
    yaml_data = read_yaml(yaml_path)
    return yaml_data.get(key, [])

def get_login_case():
    return _get_cases("auth_data.yaml", "auth_login_cases")

def get_register_case():
    return _get_cases("auth_data.yaml", "auth_register_cases")

def get_forgot_pwd_case():
    return _get_cases("auth_data.yaml", "auth_forgot_cases")

def get_user_info_cases():
    return _get_cases("personal_info_data.yaml", "user_tab_cases")

def get_user_settings_cases():
    return _get_cases("personal_info_data.yaml", "user_settings_cases")

def get_notification_privacy_cases():
    return _get_cases("personal_info_data.yaml", "notification_privacy_cases")

def get_security_cases():
    return _get_cases("personal_info_data.yaml", "security_cases")

def get_post_cases():
    return _get_cases("posts_data.yaml", "post_management_cases")

def get_comment_cases():
    return _get_cases("comments_data.yaml", "comment_management_cases")

def get_avatar_cases():
    return _get_cases("avatar_data.yaml", "avatar_cases")

def get_remove_avatar_cases():
    return _get_cases("avatar_data.yaml", "remove_avatar_cases")