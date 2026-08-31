# 阶段三：Allure 测试报告

> 生成专业、美观、信息量丰富的测试报告。

---

## 1. Allure 是什么

Allure 是一个开源的测试报告框架，可以把 pytest 的测试结果转换成漂亮的 HTML 报告。报告里可以显示：

- 测试用例的执行结果（通过/失败）
- 用例的分层结构（feature → story → test）
- 每个用例的标题、描述、严重级别
- 失败时的截图和日志附件
- 执行时间、历史趋势等

---

## 2. 安装

### 2.1 安装 Python 插件

```bash
python -m pip install allure-pytest
```

### 2.2 安装 Allure Commandline

从官网下载 zip 包，解压后把 `bin` 目录加入系统 `PATH`：

```text
D:\tools\allure-2.30.0\bin
```

验证安装：

```bash
allure --version
```

---

## 3. pytest.ini 配置

```ini
[pytest]
addopts = -n auto --reruns 2 --reruns-delay 1 --alluredir=reports/allure-results
```

`--alluredir=reports/allure-results`：指定 Allure 结果数据的输出目录。

---

## 4. 常用注解

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

---

## 5. 类结构示例

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

---

## 6. 附加截图和日志

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

---

## 7. 生成和查看报告

### 7.1 运行测试生成数据

```bash
pytest
```

### 7.2 启动报告服务

```bash
allure serve reports/allure-results
```

`allure serve` 会：

1. 把 `reports/allure-results` 里的 JSON 数据转换成 HTML
2. 启动本地服务器
3. 自动打开浏览器显示报告

---

## 8. 注意事项

- Allure 结果文件（JSON）不要提交到 Git
- 报告标题里不建议显示密码等敏感信息
- `allure-pytest` 会自动捕获 `logging` 输出，可能和手动附加的日志重复

---

> 💡 学习建议：Allure 报告最好和 Page Object、日志、截图、重试一起使用。这样 failure 时，报告里能看到完整的上下文信息。
