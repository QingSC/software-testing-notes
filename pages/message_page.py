from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MessagePage(BasePage):
    """消息显示练习页面封装类"""

    def click_show_message_button(self):
        """点击显示欢迎消息按钮"""
        self.driver.logger.info("点击显示欢迎消息按钮")
        self.driver.find_element(By.ID, "showMessageBtn").click()

    def get_message_text(self):
        """获取消息显示文本"""
        text = self.driver.find_element(By.ID, "messageDisplay").text
        self.driver.logger.info(f"消息文本：{text}")
        return text

    def get_message_class(self):
        """获取消息元素的 class 属性"""
        class_value = self.driver.find_element(By.ID, "messageDisplay").get_attribute("class")
        self.driver.logger.info(f"消息元素 class：{class_value}")
        return class_value
