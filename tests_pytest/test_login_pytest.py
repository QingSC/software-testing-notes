import pytest
import yaml
import os
from pages.login_page import LoginPage
import allure

pytestmark = [pytest.mark.login, pytest.mark.smoke]

def load_login_data():
    """从 YAML 文件加载登录测试数据"""
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 上一层目录就是项目根目录，再进入 data 目录
    data_dir = os.path.join(current_dir, "..", "data")
    # 拼接 YAML 文件完整路径
    data_file = os.path.join(data_dir, "login_data.yaml")

    # 读取 YAML 文件
    with open(data_file,"r",encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 把 YAML 数据转换成元组列表
    return [
        (case["username"], case["password"], case["expected"])
        for case in data["login_cases"]
    ]

@allure.feature("登录功能")
@allure.story("用户名密码验证")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """登录测试类"""
    @allure.title("登录测试：用户名={username}，预期={expected}")
    @allure.description("验证不同用户名密码组合的登录结果")
    @pytest.mark.parametrize("username,password,expected", load_login_data())
    def test_login(self, driver, username, password, expected):
        """参数化登录测试：使用 Page Object 封装"""
        driver.logger.info(f"测试数据：用户名={username}，密码={password}")

        page = LoginPage(driver)
        page.open()
        page.login(username, password)

        result = page.get_result()
        assert expected in result, f"期望包含'{expected}'，实际显示：{result}"
