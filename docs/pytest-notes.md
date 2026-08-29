# pytest 学习笔记

> 本项目 pytest 实践的速查笔记，忘了的时候可以翻一翻。

---

## 1. 安装与验证

```bash
# 安装 pytest
pip install pytest

# 验证安装
pytest --version
```

---

## 2. 测试发现规则

pytest 默认会自动找测试：

- 文件名：`test_*.py` 或 `*_test.py`
- 函数名：`test_` 开头
- 类名：`Test` 开头（本项目主要用函数，暂不涉及类）

示例：

```python
# test_demo.py
def test_add():
    assert 1 + 1 == 2
```

---

## 3. 常用运行命令

```bash
# 运行当前目录下所有测试
pytest

# 详细输出（推荐）
pytest -v

# 显示 print() 输出
pytest -s

# 运行指定文件
pytest test_login_pytest.py

# 运行指定函数
pytest test_login_pytest.py::test_login

# 按标记筛选
pytest -m login
pytest -m smoke

# 生成 HTML 报告
pytest --html=report.html --self-contained-html

# 并行执行（需安装 pytest-xdist）
pytest -n 2
pytest -n auto
```

---

## 4. assert 断言

pytest 直接用 Python 的 `assert`，不用额外导入。

```python
def test_login_success(practice_page):
    result = practice_page.find_element(By.ID, "loginResult").text
    assert "登录成功" in result
```

### 带自定义错误信息

```python
assert "登录成功" in result, f"期望包含'登录成功'，实际显示：{result}"
```

---

## 5. Fixture 固定装置

### 基本写法

```python
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """创建浏览器，测试结束后关闭"""
    driver = webdriver.Edge()
    yield driver       # 把 driver 交给测试函数
    driver.quit()      # 测试结束后执行
```

### 在 conftest.py 中定义

`tests_pytest/conftest.py` 里的 fixture 会被该文件夹下所有测试自动使用。

```python
# tests_pytest/conftest.py
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()


@pytest.fixture
def practice_page(driver):
    driver.get("file:///D:/Projects/software-testing-notes/pages/practice.html")
    return driver
```

### fixture 作用域

```python
@pytest.fixture(scope="function")   # 默认：每个测试函数执行一次
@pytest.fixture(scope="class")      # 每个测试类执行一次
@pytest.fixture(scope="module")     # 每个模块执行一次
@pytest.fixture(scope="session")    # 整个测试会话执行一次
```

本项目目前用 `function`（默认），每个测试独立打开关闭浏览器。

---

## 6. 参数化 @pytest.mark.parametrize

一套逻辑，多组数据：

```python
import pytest


@pytest.mark.parametrize("username,password,expected", [
    ("admin", "123456", "登录成功"),
    ("", "123456", "请输入用户名"),
    ("admin", "", "请输入密码"),
])
def test_login(practice_page, username, password, expected):
    # 输入用户名密码...
    result = practice_page.find_element(By.ID, "loginResult").text
    assert expected in result
```

pytest 会把每组数据当成一个独立用例运行。

---

## 7. 标记 Markers

### 给单个函数加标记

```python
import pytest


@pytest.mark.login
@pytest.mark.smoke
def test_login_success(practice_page):
    ...
```

### 给整个文件加标记

```python
# 文件顶部
import pytest
pytestmark = pytest.mark.login

# 多个标记用列表
pytestmark = [pytest.mark.login, pytest.mark.smoke]
```

### 常用内置标记

```python
@pytest.mark.skip(reason="暂时跳过")
@pytest.mark.xfail(reason="预期失败，已知 bug")
```

### 注册标记（避免警告）

在 `pytest.ini` 中：

```ini
[pytest]
markers =
    login: 登录相关测试
    smoke: 冒烟测试
    alert: 弹窗相关测试
```

### 按标记运行

```bash
pytest -m login
pytest -m "login or smoke"
pytest -m "not slow"    # 排除 slow 标记的用例
```

---

## 8. pytest.ini 常用配置

```ini
[pytest]
# 指定测试搜索路径
 testpaths = tests_pytest

# 注册自定义标记
markers =
    login: 登录相关测试
    alert: 弹窗相关测试
    smoke: 冒烟测试
```

---

## 9. Page Object 设计模式

把元素定位和业务操作封装到 `pages/` 目录的类里。

### 基类 BasePage

```python
# pages/base_page.py
import os


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "../pages/practice.html")
        file_path = os.path.abspath(file_path)
        self.driver.get(f"file:///{file_path}")
```

### 具体页面类

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    def input_username(self, username):
        element = self.driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys(username)

    def input_password(self, password):
        element = self.driver.find_element(By.ID, "password")
        element.clear()
        element.send_keys(password)

    def click_login(self):
        self.driver.find_element(By.ID, "loginBtn").click()

    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    def get_result(self):
        return self.driver.find_element(By.ID, "loginResult").text
```

### 测试中使用

```python
# tests_pytest/test_login_pytest.py
from pages.login_page import LoginPage


def test_login_success(driver):
    page = LoginPage(driver)
    page.open()
    page.login("admin", "123456")

    assert "登录成功" in page.get_result()
```

---

## 10. HTML 报告

### 安装

```bash
pip install pytest-html
```

### 生成报告

```bash
pytest --html=report.html --self-contained-html
```

`--self-contained-html` 让样式内嵌，只生成一个文件。

---

## 11. 并行执行

### 安装

```bash
pip install pytest-xdist
```

### 运行

```bash
pytest -n 2        # 2 个进程并行
pytest -n auto     # 自动根据 CPU 决定
```

注意：并行执行时浏览器窗口会同时弹出多个。

---

## 12. 常见错误排查

| 错误 | 原因 | 解决 |
|---|---|---|
| `NoSuchElementException` | 元素没找到 | 检查 ID/定位器；确认 `page.open()` 已调用；加显式等待 |
| `AssertionError` | 断言失败 | 看错误信息里的实际值，检查预期值是否正确 |
| `fixture 'xxx' not found` | fixture 不存在 | 检查 `conftest.py` 或参数名拼写 |
| `PytestUnknownMarkWarning` | 标记未注册 | 在 `pytest.ini` 中注册 |
| 测试运行了旧代码 | 文件没保存 | 保存后再运行 |

---

## 13. 项目文件结构参考

```text
software-testing-notes/
├── pages/                  ← Page Object 类
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── ...
├── tests_pytest/           ← pytest 测试
│   ├── conftest.py
│   ├── test_login_pytest.py
│   └── ...
├── tests/                  ← 旧 Selenium 脚本（未重构）
├── pages/practice.html     ← 本地练习页面
├── pytest.ini              ← pytest 配置
└── report.html             ← 生成的报告
```

---

> 💡 学习建议：先掌握 `assert`、fixture、parametrize、markers 这四个核心，再学 Page Object 和报告。
