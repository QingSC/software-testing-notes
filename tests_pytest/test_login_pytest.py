import pytest
from pages.login_page import LoginPage
import allure

pytestmark = [pytest.mark.login, pytest.mark.smoke]

@allure.feature("登录功能")
@allure.story("用户名密码验证")
@allure.severity(allure.severity_level.CRITICAL)

class TestLogin:
    """登录测试类"""
    @allure.title("登录测试：用户名={username}，预期={expected}")
    @allure.description("验证不同用户名密码组合的登录结果")

    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "123456", "登录成功"),
        ("", "123456", "请输入用户名"),
        ("admin", "", "请输入密码"),
        ("wronguser", "123456", "用户名或密码错误"),
        ("admin", "wrongpwd", "用户名或密码错误"),
    ])
    def test_login(self,driver, username, password, expected):
        """参数化登录测试：使用 Page Object 封装"""
        driver.logger.info(f"测试数据：用户名={username}，密码={password}")

        page = LoginPage(driver)
        page.open()
        page.login(username, password)

        result = page.get_result()
        assert expected in result, f"期望包含'{expected}'，实际显示：{result}"
