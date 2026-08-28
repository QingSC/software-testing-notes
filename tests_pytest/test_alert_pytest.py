from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import pytest
pytestmark = [pytest.mark.alert,pytest.mark.smoke]


def test_alert_text_and_accept(practice_page):
    """测试 Alert 弹窗文字，并点击确定"""
    # 点击弹出 Alert 按钮
    practice_page.find_element(By.ID, "alertBtn").click()

    # 显式等待弹窗出现
    wait = WebDriverWait(practice_page, 10)
    wait.until(EC.alert_is_present())

    # 切换到 Alert 弹窗
    alert = Alert(practice_page)

    # 断言弹窗文字
    assert alert.text == "这是一个 Alert 弹窗！", f"弹窗文字不符：{alert.text}"

    # 点击确定关闭弹窗
    alert.accept()


def test_confirm_accept(practice_page):
    """测试 Confirm 弹窗点击确定"""
    practice_page.find_element(By.ID, "confirmBtn").click()

    wait = WebDriverWait(practice_page, 10)
    wait.until(EC.alert_is_present())

    confirm = Alert(practice_page)
    confirm.accept()

    # 断言页面显示确定结果
    result = practice_page.find_element(By.ID, "confirmResult").text
    assert result == "✅ 你点击了“确定”", f"确定结果不符：{result}"


def test_confirm_dismiss(practice_page):
    """测试 Confirm 弹窗点击取消"""
    practice_page.find_element(By.ID, "confirmBtn").click()

    wait = WebDriverWait(practice_page, 10)
    wait.until(EC.alert_is_present())

    confirm = Alert(practice_page)
    confirm.dismiss()

    # 断言页面显示取消结果
    result = practice_page.find_element(By.ID, "confirmResult").text
    assert result == "❌ 你点击了“取消”", f"取消结果不符：{result}"
