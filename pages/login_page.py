from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面封装类"""

    def input_username(self, username):
        """输入用户名"""
        self.driver.logger.info(f"输入用户名：{username}")
        element = self.driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys(username)

    def input_password(self, password):
        """输入密码"""
        self.driver.logger.info(f"输入密码：{password}")
        element = self.driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys(password)

    def click_login(self):
        """点击登录按钮"""
        self.driver.logger.info("点击登录按钮")
        self.driver.find_element(By.ID, "loginBtn").click()

    def get_result(self):
        """获取登录结果文本"""
        result = self.driver.find_element(By.ID, "loginResult").text
        self.driver.logger.info(f"获取登录结果：{result}")
        return result

    def login(self, username, password):
        """完整的登录操作：输入用户名密码并点击登录"""
        self.driver.logger.info(f"执行登录操作：用户名={username}")
        self.input_username(username)
        self.input_password(password)
        self.click_login()
