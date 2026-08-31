import allure
import pytest
from pages.alert_page import AlertPage


pytestmark = [pytest.mark.alert, pytest.mark.smoke]


@allure.feature("弹窗功能")
@allure.story("Alert 与 Confirm 弹窗操作")
@allure.severity(allure.severity_level.CRITICAL)
class TestAlert:
    """弹窗测试类"""

    @allure.title("Alert 弹窗文字与确定")
    @allure.description("测试 Alert 弹窗文字，并点击确定")
    def test_alert_text_and_accept(self, driver):
        page = AlertPage(driver)
        page.open()

        page.click_alert_button()
        page.wait_for_alert()

        alert = page.get_alert()
        assert alert.text == "这是一个 Alert 弹窗！", f"弹窗文字不符：{alert.text}"
        alert.accept()

    @allure.title("Confirm 弹窗点击确定")
    @allure.description("测试 Confirm 弹窗点击确定后的结果")
    def test_confirm_accept(self, driver):
        page = AlertPage(driver)
        page.open()

        page.click_confirm_button()
        page.wait_for_alert()

        page.get_alert().accept()

        result = page.get_confirm_result_text()
        assert result == "✅ 你点击了“确定”", f"确定结果不符：{result}"

    @allure.title("Confirm 弹窗点击取消")
    @allure.description("测试 Confirm 弹窗点击取消后的结果")
    def test_confirm_dismiss(self, driver):
        page = AlertPage(driver)
        page.open()

        page.click_confirm_button()
        page.wait_for_alert()

        page.get_alert().dismiss()

        result = page.get_confirm_result_text()
        assert result == "❌ 你点击了“取消”", f"取消结果不符：{result}"
