import pytest
from pages.login_page import LoginPage


pytestmark = [pytest.mark.login, pytest.mark.smoke]


@pytest.mark.parametrize("username,password,expected", [
    ("admin", "123456", "登录成功"),
    ("", "123456", "请输入用户名"),
    ("admin", "", "请输入密码"),
    ("wronguser", "123456", "用户名或密码错误"),
    ("admin", "wrongpwd", "用户名或密码错误"),
])
def test_login(driver, username, password, expected):
    """参数化登录测试：使用 Page Object 封装"""
    page = LoginPage(driver)
    page.open()
    page.login(username, password)

    result = page.get_result()
    assert expected in result, f"期望包含'{expected}'，实际显示：{result}"
