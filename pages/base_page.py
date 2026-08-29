import os


class BasePage:
    """所有 Page 类的基类，封装公共方法"""

    def __init__(self, driver):
        """初始化时传入浏览器驱动"""
        self.driver = driver

    def open(self):
        """打开本地练习页面 practice.html"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "../pages/practice.html")
        file_path = os.path.abspath(file_path)
        self.driver.get(f"file:///{file_path}")
