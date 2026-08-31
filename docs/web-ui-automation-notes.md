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
