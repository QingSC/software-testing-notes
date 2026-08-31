import os


class BasePage:
    """所有 Page 类的基类，封装公共方法"""

    def __init__(self, driver):
        """初始化时传入浏览器驱动"""
        self.driver = driver

    def open(self):
        """打开配置文件中指定的练习页面"""
        # 从 driver 上挂载的配置中读取页面地址
        file_path = self.driver.config.get("base_url")
        self.driver.logger.info(f"打开页面：{file_path}")
        self.driver.get(f"file:///{file_path}")
