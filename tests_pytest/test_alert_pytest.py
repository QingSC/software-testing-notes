import pytest
from pages.alert_page import AlertPage


pytestmark = [pytest.mark.alert, pytest.mark.smoke]


def test_alert_text_and_accept(driver):
    """测试 Alert 弹窗文字，并点击确定"""
    page = AlertPage(driver)
    page.open()

    page.click_alert_button()
    page.wait_for_alert()

    alert = page.get_alert()
    assert alert.text == "这是一个 Alert 弹窗！", f"弹窗文字不符：{alert.text}"
    alert.accept()


def test_confirm_accept(driver):
    """测试 Confirm 弹窗点击确定"""
    page = AlertPage(driver)
    page.open()

    page.click_confirm_button()
    page.wait_for_alert()

    page.get_alert().accept()

    result = page.get_confirm_result_text()
    assert result == "✅ 你点击了“确定”", f"确定结果不符：{result}"


def test_confirm_dismiss(driver):
    """测试 Confirm 弹窗点击取消"""
    page = AlertPage(driver)
    page.open()

    page.click_confirm_button()
    page.wait_for_alert()

    page.get_alert().dismiss()

    result = page.get_confirm_result_text()
    assert result == "❌ 你点击了“取消”", f"取消结果不符：{result}"
