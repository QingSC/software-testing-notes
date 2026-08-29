from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TextareaPage(BasePage):
    """文本域和动态内容练习页面封装类"""

    def input_comment(self, text):
        """在文本域输入内容"""
        element = self.driver.find_element(By.ID, "comment")
        element.clear()
        element.send_keys(text)

    def get_comment_value(self):
        """获取文本域的值"""
        return self.driver.find_element(By.ID, "comment").get_attribute("value")

    def click_update_button(self):
        """点击更新内容按钮"""
        self.driver.find_element(By.ID, "updateBtn").click()

    def get_dynamic_content_text(self):
        """获取动态内容文本"""
        return self.driver.find_element(By.ID, "dynamic-content").text

    def click_show_hidden_button(self):
        """点击显示隐藏区域按钮"""
        self.driver.find_element(By.ID, "showHiddenBtn").click()

    def is_hidden_content_displayed(self):
        """判断隐藏区域是否可见"""
        return self.driver.find_element(By.ID, "hiddenDiv").is_displayed()
