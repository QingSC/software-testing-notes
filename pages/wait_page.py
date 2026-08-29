from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class WaitPage(BasePage):
    """显式等待练习页面封装类"""

    def click_load_button(self):
        """点击加载按钮"""
        self.driver.find_element(By.ID, "loadBtn").click()

    def get_delayed_content_text(self):
        """获取延迟内容文本"""
        return self.driver.find_element(By.ID, "delayedContent").text

    def wait_for_content(self, text, timeout=10):
        """显式等待内容中出现指定文本"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.text_to_be_present_in_element((By.ID, "delayedContent"), text))

    def get_current_time_str(self, fmt="%H:%M"):
        """获取当前时间字符串"""
        return datetime.now().strftime(fmt)
