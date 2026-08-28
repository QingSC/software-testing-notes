from selenium.webdriver.common.by import By
import pytest
pytestmark = pytest.mark.textarea

def test_textarea_input(practice_page):
    """测试文本域输入内容"""
    textarea = practice_page.find_element(By.ID, "comment")
    textarea.clear()
    textarea.send_keys("自动化测试练习")

    value = textarea.get_attribute("value")
    assert value == "自动化测试练习", f"文本域内容不符：{value}"

def test_update_dynamic_content(practice_page):
    """测试点击更新按钮后动态内容显示"""

    # 先在文本域输入内容
    textarea = practice_page.find_element(By.ID, "comment")
    textarea.clear()
    textarea.send_keys("自动化测试练习")

    # 点击更新按钮
    practice_page.find_element(By.ID, "updateBtn").click()

    # 检查动态内容区
    dynamic = practice_page.find_element(By.ID, "dynamic-content")
    assert "自动化测试练习" in dynamic.text, f"动态内容不符：{dynamic.text}"

def test_show_hidden_content(practice_page):
    """测试显示隐藏区域"""
    practice_page.find_element(By.ID, "showHiddenBtn").click()

    hidden = practice_page.find_element(By.ID, "hiddenDiv")
    assert hidden.is_displayed(), "隐藏区域未显示"

def test_hide_content_again(practice_page):
    """测试再次点击后隐藏区域重新隐藏"""
    practice_page.find_element(By.ID, "showHiddenBtn").click()
    hidden = practice_page.find_element(By.ID, "hiddenDiv")

    practice_page.find_element(By.ID, "showHiddenBtn").click()
    assert not hidden.is_displayed(), "隐藏区域仍然显示"