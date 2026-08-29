import pytest
from pages.message_page import MessagePage


pytestmark = pytest.mark.message


def test_show_welcome_message(driver):
    """测试点击按钮后显示欢迎消息，并验证 class 属性"""
    page = MessagePage(driver)
    page.open()

    page.click_show_message_button()

    assert page.get_message_text() == "🎉 欢迎来到 Selenium 练习场！", f"消息文本不符"
    assert page.get_message_class() == "success", f"class 属性不符"


def test_message_persists_on_second_click(driver):
    """测试再次点击按钮后消息仍然显示"""
    page = MessagePage(driver)
    page.open()

    page.click_show_message_button()
    page.click_show_message_button()

    assert page.get_message_text() == "🎉 欢迎来到 Selenium 练习场！", f"第二次点击后消息文本不符"
