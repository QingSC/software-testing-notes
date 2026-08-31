import codecs
import logging
import os
import pytest
import allure
from selenium import webdriver


@pytest.fixture
def driver(request):
    """
    创建 Edge 浏览器驱动，并在测试结束后自动关闭。
    同时初始化当前测试用例的日志记录。
    """
    # 创建日志目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(project_root,"logs")
    os.makedirs(logs_dir,exist_ok=True)

    # 生成日志文件名
    test_name = request.node.name
    try:
        decoded_name = codecs.decode(test_name,"unicode_escape")
    except Exception:
        decoded_name = test_name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in decoded_name)
    log_file = os.path.join(logs_dir,f"{safe_name}.log")

    #配置日志
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)

    # 清空旧的 handler，避免重复
    logger.handlers = []

    # 文件 handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8",mode="w")
    file_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)



    # 创建浏览器
    driver = webdriver.Edge()
    driver.logger = logger # 把 logger 挂在 driver 上，方便测试函数使用
    driver.log_file = log_file # 把日志文件路径也挂上去，失败时方便读取

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

            # 生成截图文件名
            # pytest 在 Windows 下可能把中文参数显示为 \uXXXX 转义形式
            # 先尝试还原成真实中文，再处理非法字符
            try:
                decoded_name = codecs.decode(item.name, "unicode_escape")
            except Exception:
                decoded_name = item.name

            safe_name = "".join(
                c if c.isalnum() or c in "-_" else "_" for c in decoded_name
            )
            file_path = os.path.join(screenshots_dir, f"{safe_name}.png")

            # 截图并保存
            # 使用 get_screenshot_as_png 再手动写入文件，兼容性更好
            try:
                screenshot_bytes = driver.get_screenshot_as_png()
                with open(file_path, "wb") as f:
                    f.write(screenshot_bytes)
                print(f"\n[screenshot] 失败截图已保存：{file_path}")

                # 把截图附加到 Allure 报告
                allure.attach(
                    screenshot_bytes,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"\n[screenshot] 截图失败：{e}")

            # 把测试日志附加到 Allure 报告
            log_file = getattr(driver, "log_file", None)
            if log_file and os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    allure.attach(
                        log_content,
                        name="测试日志",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception as e:
                    print(f"\n[allure] 附加日志失败：{e}")

