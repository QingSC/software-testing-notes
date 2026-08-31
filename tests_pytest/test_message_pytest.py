import allure
import pytest
from pages.message_page import MessagePage


pytestmark = pytest.mark.message


@allure.feature("消息显示功能")
@allure.story("按钮点击后消息显示")
@allure.severity(allure.severity_level.NORMAL)
class TestMessage:
    """消息显示测试类"""

    @allure.title("显示欢迎消息")
    @allure.description("测试点击按钮后显示欢迎消息，并验证 class 属性")
    def test_show_welcome_message(self, driver):
        page = MessagePage(driver)
        page.open()

        page.click_show_message_button()

        assert page.get_message_text() == "🎉 欢迎来到 Selenium 练习场！", f"消息文本不符"
        assert page.get_message_class() == "success", f"class 属性不符"

    @allure.title("消息持久显示")
    @allure.description("测试再次点击按钮后消息仍然显示")
    def test_message_persists_on_second_click(self, driver):
        page = MessagePage(driver)
        page.open()

        page.click_show_message_button()
        page.click_show_message_button()

        assert page.get_message_text() == "🎉 欢迎来到 Selenium 练习场！", f"第二次点击后消息文本不符"
