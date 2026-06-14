# 读取YAML格式数据文件，主要实现YAML文件解析功能，将测试数据转换为 Python 字典供数据驱动使用。

import yaml
import os

# 解析为python字典
def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        print(f"DEBUG: read_yaml from {file_path} -> {data}")  # 添加这行
        return data

def get_login_data():
    # 便于代码移植，但依赖项目目录结构的固定层级
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # 得到根目录
    yaml_path = os.path.join(base_dir, 'data', 'login_data.yaml')               # 目录拼接
    data = read_yaml(yaml_path) or {}       # 返回解析成python格式的文本内容
    return data.get('login_cases', [])