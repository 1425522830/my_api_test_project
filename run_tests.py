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
    except KeyboardInterrupt:
        print("\nAllure server stopped. Exiting gracefully.")
        sys.exit(0)
    except subprocess.CalledProcessError:
        print("Failed to run allure command. Make sure Allure is installed and in PATH.")
        print("You can manually run: allure serve ./allure-results")

if __name__ == "__main__":
    main()