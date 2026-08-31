# 阶段二：失败诊断能力

> 测试失败时，能快速定位问题原因。

---

## 1. 失败自动截图

### 1.1 实现思路

用 pytest 钩子函数 `pytest_runtest_makereport`，在测试失败时截取当前浏览器页面。

### 1.2 核心代码

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

### 1.3 关键点

- `report.when == "call"`：只在测试函数执行阶段触发
- `report.failed`：只有失败时才截图
- `item.funcargs.get("driver")`：从测试参数里取 driver
- `get_screenshot_as_png()`：获取二进制截图数据
- 文件名要处理非法字符，中文要解码 Unicode 转义

---

## 2. 测试日志记录

### 2.1 为什么需要日志

- 记录测试执行过程
- 失败时快速定位问题
- 比截图更详细地展示操作步骤

### 2.2 在 fixture 里初始化 logger

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

### 2.3 日志层级设计

| 层级 | 记录内容 | 例子 |
|---|---|---|
| 测试函数 | 测试数据、测试意图 | `测试数据：用户名=admin` |
| Page Object | 页面操作细节 | `输入用户名：admin` |
| BasePage | 公共操作 | `打开页面：.../practice.html` |

### 2.4 日志级别

```python
logger.debug("调试信息")    # 最详细
logger.info("普通信息")     # 关键步骤
logger.warning("警告")
logger.error("错误")
logger.critical("严重错误")
```

---

## 3. 失败自动重试

### 3.1 安装插件

```bash
pip install pytest-rerunfailures
```

### 3.2 配置 pytest.ini

```ini
[pytest]
addopts = -n auto --reruns 2 --reruns-delay 1
```

### 3.3 参数说明

| 参数 | 含义 |
|---|---|
| `--reruns 2` | 失败后再重试 2 次 |
| `--reruns-delay 1` | 每次重试间隔 1 秒 |

### 3.4 适用场景

- 网络抖动导致的加载超时
- 动画渲染未完成
- 页面加载偶发慢

### 3.5 不适用场景

- 代码逻辑错误（重试也会失败）
- 断言条件写错（重试也会失败）
- 环境问题（需要修复环境）

---

## 4. Page Object 中的日志

### 4.1 为什么要把日志放到 Page Object

- 测试函数更关注测试意图
- 页面操作自带日志，复用性好
- 修改一处，全局生效

### 4.2 示例

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

### 4.3 日志位置的选择

| 位置 | 记录内容 | 适合场景 |
|---|---|---|
| 执行前 | 意图、参数 | 操作可能失败 |
| 执行后 | 结果、返回值 | 获取值用于断言 |
| 前后都记 | 完整生命周期 | 关键步骤 |

---

## 5. 并行执行

### 5.1 安装插件

```bash
pip install pytest-xdist
```

### 5.2 配置默认并行

```ini
[pytest]
addopts = -n auto
```

### 5.3 常用命令

```bash
pytest -n auto       # 自动根据 CPU 核心数并行
pytest -n 4          # 4 个进程并行
pytest -n 0          # 串行执行（调试推荐）
```

### 5.4 注意事项

- 并行时会同时打开多个浏览器窗口
- 每个测试应该有独立的 fixture，避免互相干扰
- 调试时建议用 `-n 0` 串行执行，方便看日志顺序

---

## 6. 项目运行产物管理

### 6.1 自动生成的目录

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

### 6.2 .gitignore 配置

```gitignore
screenshots/
logs/
reports/
report.html
.pytest_cache/
```

这些文件由测试运行时生成，不应该提交到 Git。

---

## 7. 常见问题排查

| 问题 | 可能原因 | 解决 |
|---|---|---|
| 截图没有生成 | 文件名包含非法字符 | 用 `isalnum()` 过滤 |
| 日志文件乱码 | 编码不是 UTF-8 | `encoding="utf-8"` |
| 日志重复写入 | logger handler 重复添加 | 每次清空 `logger.handlers` |
| 并行测试互相干扰 | fixture 作用域不对 | 使用 `function` 作用域 |
| 重试后还是失败 | 代码逻辑错误 | 修复代码，不是重试问题 |

---

> 💡 学习建议：这些知识不是孤立的，要结合起来用。比如失败后，先看日志定位步骤，再看截图确认页面状态，最后用重试判断是不是偶发问题。
