from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.base_page import BasePage


class AlertPage(BasePage):
    """弹窗练习页面封装类"""

    def click_alert_button(self):
        """点击弹出 Alert 按钮"""
        self.driver.find_element(By.ID, "alertBtn").click()

    def click_confirm_button(self):
        """点击弹出 Confirm 按钮"""
        self.driver.find_element(By.ID, "confirmBtn").click()

    def wait_for_alert(self, timeout=10):
        """显式等待弹窗出现"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.alert_is_present())

    def get_alert(self):
        """获取当前弹窗对象"""
        return Alert(self.driver)

    def get_confirm_result_text(self):
        """获取 Confirm 弹窗操作后的结果文本"""
        return self.driver.find_element(By.ID, "confirmResult").text
