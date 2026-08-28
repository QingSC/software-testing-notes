from selenium.webdriver.common.by import By
import pytest
pytestmark = pytest.mark.message

def test_show_welcome_message(practice_page):
    """测试点击按钮后显示欢迎消息，并验证 class 属性"""
    # 点击"显示欢迎消息"按钮
    show_btn = practice_page.find_element(By.ID, "showMessageBtn")
    show_btn.click()

    # 获取显示的消息文本
    message = practice_page.find_element(By.ID, "messageDisplay")
    assert message.text == "🎉 欢迎来到 Selenium 练习场！", f"消息文本不符：{message.text}"

    # 获取 class 属性并断言
    class_value = message.get_attribute("class")
    assert class_value == "success", f"class 属性不符：{class_value}"


def test_message_persists_on_second_click(practice_page):
    """测试再次点击按钮后消息仍然显示"""
    show_btn = practice_page.find_element(By.ID, "showMessageBtn")

    # 点击两次
    show_btn.click()
    show_btn.click()

    message = practice_page.find_element(By.ID, "messageDisplay")
    assert message.text == "🎉 欢迎来到 Selenium 练习场！", f"第二次点击后消息文本不符：{message.text}"
