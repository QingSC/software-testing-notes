from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TextareaPage(BasePage):
    """文本域和动态内容练习页面封装类"""

    def input_comment(self, text):
        """在文本域输入内容"""
        self.driver.logger.info(f"在文本域输入：{text}")
        element = self.driver.find_element(By.ID, "comment")
        element.clear()
        element.send_keys(text)

    def get_comment_value(self):
        """获取文本域的值"""
        value = self.driver.find_element(By.ID, "comment").get_attribute("value")
        self.driver.logger.info(f"文本域当前值：{value}")
        return value

    def click_update_button(self):
        """点击更新内容按钮"""
        self.driver.logger.info("点击更新内容按钮")
        self.driver.find_element(By.ID, "updateBtn").click()

    def get_dynamic_content_text(self):
        """获取动态内容文本"""
        text = self.driver.find_element(By.ID, "dynamic-content").text
        self.driver.logger.info(f"动态内容文本：{text}")
        return text

    def click_show_hidden_button(self):
        """点击显示隐藏区域按钮"""
        self.driver.logger.info("点击显示隐藏区域按钮")
        self.driver.find_element(By.ID, "showHiddenBtn").click()

    def is_hidden_content_displayed(self):
        """判断隐藏区域是否可见"""
        displayed = self.driver.find_element(By.ID, "hiddenDiv").is_displayed()
        self.driver.logger.info(f"隐藏区域可见状态：{displayed}")
        return displayed
