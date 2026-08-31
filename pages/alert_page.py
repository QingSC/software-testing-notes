from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.base_page import BasePage


class AlertPage(BasePage):
    """弹窗练习页面封装类"""

    def click_alert_button(self):
        """点击弹出 Alert 按钮"""
        self.driver.logger.info("点击弹出 Alert 按钮")
        self.driver.find_element(By.ID, "alertBtn").click()

    def click_confirm_button(self):
        """点击弹出 Confirm 按钮"""
        self.driver.logger.info("点击弹出 Confirm 按钮")
        self.driver.find_element(By.ID, "confirmBtn").click()

    def wait_for_alert(self, timeout=10):
        """显式等待弹窗出现"""
        self.driver.logger.info(f"等待弹窗出现，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.alert_is_present())
        self.driver.logger.info("弹窗已出现")

    def get_alert(self):
        """获取当前弹窗对象"""
        alert = Alert(self.driver)
        self.driver.logger.info(f"获取弹窗文本：{alert.text}")
        return alert

    def get_confirm_result_text(self):
        """获取 Confirm 弹窗操作后的结果文本"""
        text = self.driver.find_element(By.ID, "confirmResult").text
        self.driver.logger.info(f"Confirm 操作结果：{text}")
        return text
