import pytest
from pages.textarea_page import TextareaPage


pytestmark = pytest.mark.textarea


def test_textarea_input(driver):
    """测试文本域输入内容"""
    page = TextareaPage(driver)
    page.open()

    page.input_comment("自动化测试练习")
    value = page.get_comment_value()

    assert value == "自动化测试练习", f"文本域内容不符：{value}"


def test_update_dynamic_content(driver):
    """测试点击更新按钮后动态内容显示"""
    page = TextareaPage(driver)
    page.open()

    page.input_comment("自动化测试练习")
    page.click_update_button()

    text = page.get_dynamic_content_text()
    assert "自动化测试练习" in text, f"动态内容不符：{text}"


def test_show_hidden_content(driver):
    """测试显示隐藏区域"""
    page = TextareaPage(driver)
    page.open()

    page.click_show_hidden_button()
    assert page.is_hidden_content_displayed(), "隐藏区域未显示"


def test_hide_content_again(driver):
    """测试再次点击后隐藏区域重新隐藏"""
    page = TextareaPage(driver)
    page.open()

    page.click_show_hidden_button()
    page.click_show_hidden_button()
    assert not page.is_hidden_content_displayed(), "隐藏区域仍然显示"
