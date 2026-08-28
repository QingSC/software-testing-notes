import os
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    """
    创建一个 Edge 浏览器驱动，并在测试结束后自动关闭。
    这个 fixture 会被 tests_pytest 文件夹下的所有测试文件自动使用。
    """
    # 测试开始前执行：打开浏览器
    driver = webdriver.Edge() 

    # 把 driver 交给测试函数使用
    yield driver

    # 测试结束后执行：关闭浏览器
    driver.quit()

@pytest.fixture
def practice_page(driver):
    """
    使用 driver fixture，并自动打开本地练习页面 practice.html。
    测试函数直接使用 practice_page，就省去了重复写打开页面代码。
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../pages/practice.html")
    file_path = os.path.abspath(file_path)
    driver.get(f"file:///{file_path}")

    return driver