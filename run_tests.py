import subprocess
import sys

if __name__ == "__main__":
    # 执行所有测试用例，并将生成的 Allure 原始数据保存到 allure-result 目录中
    subprocess.run([
        sys.executable, "-m", "pytest",
        "testcases/",
        "--alluredir=allure-result",
        "--clean-alluredir"
    ])

    # 启动本地 Web 服务预览测试报告
    subprocess.run("allure serve allure-result", shell=True)