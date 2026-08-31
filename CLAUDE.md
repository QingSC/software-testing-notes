# Claude 项目协作说明

## 学习辅导风格

- 用户是初学者，每次教授新内容时要讲得详细，不要一笔带过。
- 每次只输出一小步，等用户说“继续”再进入下一步。
- 解释代码时说明每一行的作用，以及为什么要这样写。
- 优先使用项目内已有的练习文件和本地页面（如 `pages/practice.html`）作为示例。
- 提供的代码示例中要适当添加注释，帮助初学者理解每一部分的作用。
- 如果代码修改点很少，只列出需要修改的地方，不用重写整个文件。
- 新概念第一次出现时提供完整代码、模板和详细解释，先让用户自己尝试写；当重复性变高时，再询问是否需要我直接写。

## 项目测试基础设施

本项目使用 pytest + Selenium 进行 Web UI 自动化测试，测试文件位于 `tests_pytest/`，页面封装位于 `pages/`。

### 失败自动截图

`tests_pytest/conftest.py` 中通过 `pytest_runtest_makereport` 钩子实现：

- 当测试在执行阶段（`report.when == "call"`）失败时触发
- 从测试函数参数中获取 `driver` fixture
- 截图保存到 `tests_pytest/screenshots/`
- 文件名基于 `item.name` 生成，使用 `codecs.decode(..., "unicode_escape")` 把 pytest 的 Unicode 转义形式还原为中文
- 使用 `driver.get_screenshot_as_png()` 获取二进制数据后手动写入文件，兼容性更好

### 测试日志记录

`driver` fixture 同时为每个测试用例初始化独立的 logger：

- 日志目录：`tests_pytest/logs/`
- 每个用例生成一个独立的 `.log` 文件
- logger 通过 `driver.logger` 暴露给测试函数使用
- 日志格式：`%(asctime)s - %(levelname)s - %(message)s`
- 日志编码：`utf-8`

### 测试运行

```bash
# 默认并行执行
pytest

# 串行执行（调试推荐）
pytest -n 0
```

### 忽略的运行产物

以下目录/文件由测试运行时生成，已加入 `.gitignore`，不应提交：

- `tests_pytest/screenshots/`
- `tests_pytest/logs/`
- `reports/`
- `report.html`
- `.pytest_cache/`
