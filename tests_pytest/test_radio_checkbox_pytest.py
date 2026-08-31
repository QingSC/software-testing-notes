import allure
import pytest
from pages.radio_checkbox_page import RadioCheckboxPage


pytestmark = pytest.mark.checkbox


@allure.feature("单选框与复选框功能")
@allure.story("测试单选复选框可用")
@allure.severity(allure.severity_level.CRITICAL)
class TestRadioCheckbox:
    """单选框与复选框类"""

    @allure.title("测试选中女单选按钮")
    @allure.description("验证按钮可选中")
    def test_select_female_radio(self, driver):
        """测试选中女单选按钮"""
        page = RadioCheckboxPage(driver)
        page.open()
        page.select_female()
        assert page.is_female_selected(), "女单选按钮未被选中"

    @allure.title("测试取消选中复选框按钮")
    @allure.description("验证复选框按钮可以取消选中")
    def test_deselect_email_checkbox(self, driver):
        """测试取消邮件通知复选框"""
        page = RadioCheckboxPage(driver)
        page.open()
        page.click_value_notify("emailNotify")

        assert not page.is_value_notify_selected("emailNotify"), "邮件通知复选框仍然被选中"

    @allure.title("测试选中复选框按钮")
    @allure.description("验证复选框按钮可以选中")
    def test_select_sms_checkbox(self, driver):
        """测试选中短信通知复选框"""
        page = RadioCheckboxPage(driver)
        page.open()
        page.click_value_notify("smsNotify")

        assert page.is_value_notify_selected("smsNotify"), "短信复选框未被选中"

    @allure.title("测试微信复选框默认未选中")
    @allure.description("验证微信复选框默认状态为未选中")
    def test_wechat_checkbox_default_unchecked(self, driver):
        """测试微信通知复选框默认未选中"""
        page = RadioCheckboxPage(driver)
        page.open()
        assert not page.is_value_notify_selected("wechatNotify"), "微信复选框默认被选中"

    @allure.title("测试选中微信复选框")
    @allure.description("验证微信复选框可以选中")
    def test_select_wechat_checkbox(self, driver):
        """测试选中微信通知复选框"""
        page = RadioCheckboxPage(driver)
        page.open()
        page.click_value_notify("wechatNotify")
        assert page.is_value_notify_selected("wechatNotify"), "微信复选框未被选中"
