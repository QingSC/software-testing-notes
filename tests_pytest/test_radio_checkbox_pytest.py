from pages.radio_checkbox_page import RadioCheckboxPage
import pytest
pytestmark = pytest.mark.checkbox

def test_select_female_radio(driver):
    """测试选中女单选按钮"""
    page = RadioCheckboxPage(driver)
    page.open()
    page.select_female()
    assert page.is_female_selected(), "女单选按钮未被选中"


def test_deselect_email_checkbox(driver):
    """测试取消邮件通知复选框"""
    page = RadioCheckboxPage(driver)
    page.open()
    page.click_value_notify("emailNotify")
    
    assert not page.is_value_notify_selected("emailNotify"), "邮件通知复选框仍然被选中"


def test_select_sms_checkbox(driver):
    """测试选中短信通知复选框"""
    page = RadioCheckboxPage(driver)
    page.open()
    page.click_value_notify("smsNotify")

    assert page.is_value_notify_selected("smsNotify"), "短信复选框未被选中"


def test_wechat_checkbox_default_unchecked(driver):
    """测试微信通知复选框默认未选中"""
    page = RadioCheckboxPage(driver)
    page.open()
    assert not page.is_value_notify_selected("wechatNotify"), "微信复选框默认被选中"


def test_select_wechat_checkbox(driver):
    """测试选中微信通知复选框"""
    page = RadioCheckboxPage(driver)
    page.open()
    page.click_value_notify("wechatNotify")
    assert page.is_value_notify_selected("wechatNotify"), "微信复选框未被选中"
