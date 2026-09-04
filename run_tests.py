import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "pytest",
        "testcases/",
        "--alluredir=allure-result",
        "--clean-alluredir"
    ])
    subprocess.run("allure serve allure-result", shell=True)