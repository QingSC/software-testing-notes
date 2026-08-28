import os
from selenium.webdriver.common.by import By


class LoginPage:
    """登录页面封装类"""

    def __init__(self, driver):
        """初始化时传入浏览器驱动"""
        self.driver = driver

    def open(self):
        """打开本地登录练习页面"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "../pages/practice.html")
        file_path = os.path.abspath(file_path)
        self.driver.get(f"file:///{file_path}")

    def input_username(self, username):
        """输入用户名"""
        element = self.driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys(username)

    def input_password(self, password):
        """输入密码"""
        element = self.driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys(password)

    def click_login(self):
        """点击登录按钮"""
        self.driver.find_element(By.ID, "loginBtn").click()

    def get_result(self):
        """获取登录结果文本"""
        return self.driver.find_element(By.ID, "loginResult").text

    def login(self, username, password):
        """完整的登录操作：输入用户名密码并点击登录"""
        self.input_username(username)
        self.input_password(password)
        self.click_login()
