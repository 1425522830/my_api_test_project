# 运行所有测试的启动脚本
import subprocess
import sys

def main():
    print("Running tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "testcases/",
        "--alluredir=./allure-results",
        "--clean-alluredir"
    ])

    if result.returncode != 0:
        print("Tests failed. Check the output.")
    print("Generating and opening Allure report...")

    try:
        subprocess.run("allure serve ./allure-results", shell=True, check=True)
    except FileNotFoundError:
        print("Allure 未安装或不在 PATH 中。请安装 Allure 并添加到环境变量。")
        print("你可以手动运行: allure serve ./allure-results")
    except KeyboardInterrupt:
        print("\nAllure server stopped. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()