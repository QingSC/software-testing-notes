from selenium.webdriver.common.by import By
import pytest
pytestmark = pytest.mark.checkbox

def test_select_female_radio(practice_page):
    """测试选中女单选按钮"""
    female_radio = practice_page.find_element(By.ID, "female")
    female_radio.click()

    assert female_radio.is_selected(), "女单选按钮未被选中"


def test_deselect_email_checkbox(practice_page):
    """测试取消邮件通知复选框"""
    email_checkbox = practice_page.find_element(By.ID, "emailNotify")
    email_checkbox.click()

    assert not email_checkbox.is_selected(), "邮件通知复选框仍然被选中"


def test_select_sms_checkbox(practice_page):
    """测试选中短信通知复选框"""
    sms_checkbox = practice_page.find_element(By.ID, "smsNotify")
    sms_checkbox.click()

    assert sms_checkbox.is_selected(), "短信复选框未被选中"


def test_wechat_checkbox_default_unchecked(practice_page):
    """测试微信通知复选框默认未选中"""
    wechat_checkbox = practice_page.find_element(By.ID, "wechatNotify")

    assert not wechat_checkbox.is_selected(), "微信复选框默认被选中"


def test_select_wechat_checkbox(practice_page):
    """测试选中微信通知复选框"""
    wechat_checkbox = practice_page.find_element(By.ID, "wechatNotify")
    wechat_checkbox.click()

    assert wechat_checkbox.is_selected(), "微信复选框未被选中"
