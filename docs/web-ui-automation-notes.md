# Web UI 自动化测试深化笔记

> 记录从基础脚本到工程化测试过程中学到的关键知识点，方便复习和查阅。

---

## 1. 测试用例设计方法

### 1.1 等价类划分

把输入数据分成有效类和无效类，每类选一个代表测试。

**例子：登录用户名**

| 等价类 | 代表数据 | 预期结果 |
|---|---|---|
| 有效类 | `admin` | 继续验证密码 |
| 无效类-空 | `""` | 提示"请输入用户名" |
| 无效类-错误 | `wronguser` | 提示"用户名或密码错误" |

### 1.2 边界值分析

错误往往发生在边界上，要测边界点及其附近值。

**例子：密码长度要求 6-20 位**

| 测试数据 | 长度 | 预期结果 |
|---|---|---|
| `12345` | 5 位 | 失败，密码太短 |
| `123456` | 6 位 | 成功（下边界） |
| `...20位...` | 20 位 | 成功（上边界） |
| `...21位...` | 21 位 | 失败，密码太长 |

### 1.3 判定表驱动法

多个条件组合影响结果时，列出所有组合。

**例子：登录**

| 用户名正确 | 密码正确 | 预期结果 |
|---|---|---|
| 是 | 是 | 登录成功 |
| 是 | 否 | 用户名或密码错误 |
| 否 | 是 | 用户名或密码错误 |
| 否 | 否 | 用户名或密码错误 |

### 1.4 错误推测法

根据经验预测容易出错的地方。

**例子：**

- 用户名前后带空格
- 快速连续点击按钮
- 大小写敏感
- 复制粘贴带换行符

### 1.5 场景法

模拟用户完整操作流程。

**例子：**

1. 登录
2. 选择城市
3. 填写评论
4. 点击更新
5. 查看动态内容

---

## 2. 失败自动截图

### 2.1 实现思路

用 pytest 钩子函数 `pytest_runtest_makereport`，在测试失败时截取当前浏览器页面。

### 2.2 核心代码

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # 生成合法文件名
            test_name = item.name
            safe_name = "".join(
                c if c.isalnum() or c in "-_" else "_" for c in test_name
            )
            file_path = os.path.join(screenshots_dir, f"{safe_name}.png")

            # 截图并保存
            screenshot_bytes = driver.get_screenshot_as_png()
            with open(file_path, "wb") as f:
                f.write(screenshot_bytes)
```

### 2.3 关键点

- `report.when == "call"`：只在测试函数执行阶段触发
- `report.failed`：只有失败时才截图
- `item.funcargs.get("driver")`：从测试参数里取 driver
- `get_screenshot_as_png()`：获取二进制截图数据
- 文件名要处理非法字符，中文要解码 Unicode 转义

---

## 3. 测试日志记录

### 3.1 为什么需要日志

- 记录测试执行过程
- 失败时快速定位问题
- 比截图更详细地展示操作步骤

### 3.2 在 fixture 里初始化 logger

```python
@pytest.fixture
def driver(request):
    # 创建日志目录
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # 生成日志文件名
    test_name = request.node.name
    log_file = os.path.join(logs_dir, f"{test_name}.log")

    # 配置 logger
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)
    logger.handlers = []  # 清空旧 handler

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    # 创建浏览器并把 logger 挂上去
    driver = webdriver.Edge()
    driver.logger = logger

    yield driver
    driver.quit()
```

### 3.3 日志层级设计

| 层级 | 记录内容 | 例子 |
|---|---|---|
| 测试函数 | 测试数据、测试意图 | `测试数据：用户名=admin` |
| Page Object | 页面操作细节 | `输入用户名：admin` |
| BasePage | 公共操作 | `打开页面：.../practice.html` |

### 3.4 日志级别

```python
logger.debug("调试信息")    # 最详细
logger.info("普通信息")     # 关键步骤
logger.warning("警告")
logger.error("错误")
logger.critical("严重错误")
```

---

## 4. 失败自动重试

### 4.1 安装插件

```bash
pip install pytest-rerunfailures
```

### 4.2 配置 pytest.ini

```ini
[pytest]
addopts = -n auto --reruns 2 --reruns-delay 1
```

### 4.3 参数说明

| 参数 | 含义 |
|---|---|
| `--reruns 2` | 失败后再重试 2 次 |
| `--reruns-delay 1` | 每次重试间隔 1 秒 |

### 4.4 适用场景

- 网络抖动导致的加载超时
- 动画渲染未完成
- 页面加载偶发慢

### 4.5 不适用场景

- 代码逻辑错误（重试也会失败）
- 断言条件写错（重试也会失败）
- 环境问题（需要修复环境）

---

## 5. Page Object 中的日志

### 5.1 为什么要把日志放到 Page Object

- 测试函数更关注测试意图
- 页面操作自带日志，复用性好
- 修改一处，全局生效

### 5.2 示例

```python
class LoginPage(BasePage):
    def input_username(self, username):
        self.driver.logger.info(f"输入用户名：{username}")
        element = self.driver.find_element(By.ID, "username")
        element.clear()
        element.send_keys(username)

    def get_result(self):
        result = self.driver.find_element(By.ID, "loginResult").text
        self.driver.logger.info(f"获取登录结果：{result}")
        return result
```

### 5.3 日志位置的选择

| 位置 | 记录内容 | 适合场景 |
|---|---|---|
| 执行前 | 意图、参数 | 操作可能失败 |
| 执行后 | 结果、返回值 | 获取值用于断言 |
| 前后都记 | 完整生命周期 | 关键步骤 |

---

## 6. 并行执行

### 6.1 安装插件

```bash
pip install pytest-xdist
```

### 6.2 配置默认并行

```ini
[pytest]
addopts = -n auto
```

### 6.3 常用命令

```bash
pytest -n auto       # 自动根据 CPU 核心数并行
pytest -n 4          # 4 个进程并行
pytest -n 0          # 串行执行（调试推荐）
```

### 6.4 注意事项

- 并行时会同时打开多个浏览器窗口
- 每个测试应该有独立的 fixture，避免互相干扰
- 调试时建议用 `-n 0` 串行执行，方便看日志顺序

---

## 7. 项目运行产物管理

### 7.1 自动生成的目录

```text
software-testing-notes/
├── tests_pytest/
│   ├── screenshots/    # 失败截图
│   ├── logs/           # 测试日志
│   └── ...
├── reports/            # 测试报告
├── report.html         # HTML 报告
└── .pytest_cache/      # pytest 缓存
```

### 7.2 .gitignore 配置

```gitignore
screenshots/
logs/
reports/
report.html
.pytest_cache/
```

这些文件由测试运行时生成，不应该提交到 Git。

---

## 8. 常见问题排查

| 问题 | 可能原因 | 解决 |
|---|---|---|
| 截图没有生成 | 文件名包含非法字符 | 用 `isalnum()` 过滤 |
| 日志文件乱码 | 编码不是 UTF-8 | `encoding="utf-8"` |
| 日志重复写入 | logger handler 重复添加 | 每次清空 `logger.handlers` |
| 并行测试互相干扰 | fixture 作用域不对 | 使用 `function` 作用域 |
| 重试后还是失败 | 代码逻辑错误 | 修复代码，不是重试问题 |

---

> 💡 学习建议：这些知识不是孤立的，要结合起来用。比如失败后，先看日志定位步骤，再看截图确认页面状态，最后用重试判断是不是偶发问题。

---

## 9. Allure 测试报告

### 9.1 Allure 是什么

Allure 是一个开源的测试报告框架，可以把 pytest 的测试结果转换成漂亮的 HTML 报告。报告里可以显示：

- 测试用例的执行结果（通过/失败）
- 用例的分层结构（feature → story → test）
- 每个用例的标题、描述、严重级别
- 失败时的截图和日志附件
- 执行时间、历史趋势等

### 9.2 安装

**安装 Python 插件：**

```bash
python -m pip install allure-pytest
```

**安装 Allure Commandline：**

从官网下载 zip 包，解压后把 `bin` 目录加入系统 `PATH`：

```text
D:\tools\allure-2.30.0\bin
```

验证安装：

```bash
allure --version
```

### 9.3 pytest.ini 配置

```ini
[pytest]
addopts = -n auto --reruns 2 --reruns-delay 1 --alluredir=reports/allure-results
```

`--alluredir=reports/allure-results`：指定 Allure 结果数据的输出目录。

### 9.4 常用注解

| 注解 | 作用 | 层级 |
|---|---|---|
| `@allure.feature("登录功能")` | 大功能模块 | 类上 |
| `@allure.story("用户名密码验证")` | 用户故事 | 类上 |
| `@allure.title("登录测试")` | 用例标题 | 方法上 |
| `@allure.description("描述文字")` | 用例描述 | 方法上 |
| `@allure.severity(allure.severity_level.CRITICAL)` | 严重程度 | 类或方法上 |

严重级别：

```text
BLOCKER  → 阻塞级别
CRITICAL → 关键
NORMAL   → 普通
MINOR    → 次要
TRIVIAL  → 轻微
```

### 9.5 类结构示例

```python
import allure
import pytest


@allure.feature("登录功能")
@allure.story("用户名密码验证")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """登录测试类"""

    @allure.title("登录测试：用户名={username}")
    @allure.description("验证不同用户名密码组合的登录结果")
    @pytest.mark.parametrize("username,password,expected", [...])
    def test_login(self, driver, username, password, expected):
        ...
```

注意：方法在类里时，第一个参数要写成 `self`。

### 9.6 附加截图和日志

在 `conftest.py` 的 `pytest_runtest_makereport` 钩子中，失败时附加到 Allure：

```python
import allure

# 附加截图
allure.attach(
    screenshot_bytes,
    name="失败截图",
    attachment_type=allure.attachment_type.PNG
)

# 附加日志文本
allure.attach(
    log_content,
    name="测试日志",
    attachment_type=allure.attachment_type.TEXT
)
```

### 9.7 生成和查看报告

**运行测试生成数据：**

```bash
pytest
```

**启动报告服务：**

```bash
allure serve reports/allure-results
```

`allure serve` 会：

1. 把 `reports/allure-results` 里的 JSON 数据转换成 HTML
2. 启动本地服务器
3. 自动打开浏览器显示报告

### 9.8 注意事项

- Allure 结果文件（JSON）不要提交到 Git
- 报告标题里不建议显示密码等敏感信息
- `allure-pytest` 会自动捕获 `logging` 输出，可能和手动附加的日志重复

---

> 💡 学习建议：Allure 报告最好和 Page Object、日志、截图、重试一起使用。这样 failure 时，报告里能看到完整的上下文信息。

---

## 10. 测试数据与配置分离

### 10.1 为什么需要分离

原来测试数据、页面地址、浏览器类型都直接写在代码里。这样有几个问题：

- 改测试数据要改代码
- 换环境要改多处代码
- 代码和配置混在一起，不好维护

分离后：

- 数据放在 YAML/JSON 文件
- 配置放在 JSON 文件
- 代码只负责业务逻辑

### 10.2 数据分离：YAML

把登录测试的参数化数据抽到 `data/login_data.yaml`：

```yaml
login_cases:
  - username: admin
    password: "123456"
    expected: 登录成功

  - username: ""
    password: "123456"
    expected: 请输入用户名
```

测试代码里读取：

```python
import yaml
import os


def load_login_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "..", "data", "login_data.yaml")

    with open(data_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return [
        (case["username"], case["password"], case["expected"])
        for case in data["login_cases"]
    ]


@pytest.mark.parametrize("username,password,expected", load_login_data())
def test_login(self, driver, username, password, expected):
    ...
```

### 10.3 配置分离：JSON

创建 `config/dev.json` 和 `config/test.json`：

```json
{
  "browser": "edge",
  "base_url": "../pages/practice.html"
}
```

### 10.4 支持命令行选择环境

在 `conftest.py` 里添加：

```python
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="测试环境：dev/test"
    )
```

读取配置：

```python
def load_config(env="dev"):
    config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
    config_file = os.path.join(config_dir, f"{env}.json")

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 把相对路径转成绝对路径
    base_url = config.get("base_url", "../pages/practice.html")
    config["base_url"] = os.path.abspath(os.path.join(config_dir, base_url))

    return config
```

### 10.5 driver fixture 使用配置

```python
@pytest.fixture
def driver(request):
    env = request.config.getoption("--env")
    config = load_config(env)

    browser = config.get("browser", "edge").lower()
    if browser == "edge":
        driver = webdriver.Edge()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"不支持的浏览器类型：{browser}")

    driver.config = config
    ...
```

### 10.6 Page Object 使用配置

```python
def open(self):
    file_path = self.driver.config.get("base_url")
    self.driver.logger.info(f"打开页面：{file_path}")
    self.driver.get(f"file:///{file_path}")
```

### 10.7 运行方式

```bash
pytest                  # 默认使用 dev 环境
pytest --env=test      # 使用 test 环境
pytest --env=dev       # 使用 dev 环境
```

### 10.8 注意事项

- YAML 里的数字密码要加引号，避免被解析成数字
- JSON 文件里不能写注释
- 配置文件也不要提交到 Git（如果包含敏感信息）
- `pytest_addoption` 是 pytest 固定名字的钩子函数

---

> 💡 学习建议：数据和配置分离后，测试代码会更干净。但不要把所有东西都抽到配置文件里，只有会变化的内容才适合放到配置中。
