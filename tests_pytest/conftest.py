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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子函数：在每个测试用例执行完成后触发。
    如果测试在执行阶段（call）失败，自动截取当前浏览器页面截图。
    """
    # 先执行测试用例本身
    outcome = yield

    # 获取测试结果对象
    report = outcome.get_result()

    # 只在测试函数执行阶段且失败时截图
    if report.when == "call" and report.failed:
        # 从测试函数的参数里取出 driver fixture
        driver = item.funcargs.get("driver")

        if driver:
            # 使用项目根目录作为截图保存路径
            project_root = os.path.dirname(os.path.abspath(__file__))
            screenshots_dir = os.path.join(project_root, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            # 生成截图文件名：用例名里的非安全字符替换为下划线
            # 参数化用例名可能包含中文、方括号、空格等，需要处理成合法文件名
            test_name = item.name
            safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
            file_path = os.path.join(screenshots_dir, f"{safe_name}.png")

            # 截图并保存
            # 使用 get_screenshot_as_png 再手动写入文件，兼容性更好
            try:
                screenshot_bytes = driver.get_screenshot_as_png()
                with open(file_path, "wb") as f:
                    f.write(screenshot_bytes)
                print(f"\n[screenshot] 失败截图已保存：{file_path}")
            except Exception as e:
                print(f"\n[screenshot] 截图失败：{e}")
