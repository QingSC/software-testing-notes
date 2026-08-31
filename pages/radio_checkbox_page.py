from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RadioCheckboxPage(BasePage):
    """单选按钮和复选框练习页面封装类"""

    def select_female(self):
        """选中女单选按钮"""
        self.driver.logger.info("选中女单选按钮")
        self.driver.find_element(By.ID, "female").click()

    def is_female_selected(self):
        """判断女单选按钮是否被选中"""
        selected = self.driver.find_element(By.ID, "female").is_selected()
        self.driver.logger.info(f"女单选按钮选中状态：{selected}")
        return selected

    def click_value_notify(self, value):
        """按 value 点击通知复选框"""
        self.driver.logger.info(f"点击通知复选框：{value}")
        self.driver.find_element(By.ID, value).click()

    def is_value_notify_selected(self, value):
        """判断 value 通知复选框是否被选中"""
        selected = self.driver.find_element(By.ID, value).is_selected()
        self.driver.logger.info(f"通知复选框 {value} 选中状态：{selected}")
        return selected
