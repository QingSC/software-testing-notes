# pytest 学习流程指南

> 基于本项目的 Selenium Web 自动化测试练习内容，整理的一份 pytest 学习路线图。

---

## 阶段一：pytest 基础入门

**目标**：让单个脚本能在 pytest 中跑起来。

- 安装 pytest：`pip install pytest`
- 测试函数命名必须以 `test_` 开头
- 运行方式：
  - `pytest` — 默认运行
  - `pytest -v` — 详细输出
  - `pytest -s` — 显示 print 内容
- 使用 `assert` 做断言，替代原来的 `print` 判断
- pytest 自动发现规则：默认查找 `test_*.py` 或 `*_test.py`

**实践**：把 `test_baidu.py` 改成 pytest 格式，用 `assert` 判断百度搜索后的页面标题。

---

## 阶段二：重构现有 Selenium 脚本

**目标**：把当前 `tests/` 下的 9 个脚本全部改为 pytest 测试函数。

- 删除 `if __name__ == '__main__':` 入口
- 每个脚本的核心操作拆成独立的 `test_xxx()` 函数
- 一个函数只测一个场景，断言要明确

**对应练习**：

| 原脚本 | 重构后测试点 |
|---|---|
| `test_local.py` | 登录表单成功 / 失败断言 |
| `text_local_2.py` | Select 下拉框选中项断言 |
| `text_local_3.py` | 单选按钮 / 复选框状态断言 |
| `text_local_4.py` | 文本域内容、动态内容显示断言 |
| `text_local_5.py` | 表格数据遍历与断言 |
| `text_local_6.py` | 显式等待后元素出现断言 |
| `text_local_7.py` | 交互反馈文本 / 属性断言 |
| `text_local_8.py` | Alert / Confirm 弹窗文本与接受断言 |

---

## 阶段三：Fixture 管理 WebDriver

**目标**：统一创建和关闭浏览器，避免每个脚本都写一遍。

- 学习 `@pytest.fixture`
- fixture 里完成 `driver = webdriver.Edge(...)`
- teardown 用 `yield` 分隔，最后执行 `driver.quit()`
- 把公共 fixture 放到 `tests/conftest.py`，所有测试文件自动可用
- 理解 `scope`：function（默认）/ class / module / session

**实践**：在 `tests/conftest.py` 中定义：

```python
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()
```

然后每个测试函数直接写：

```python
def test_local(driver):
    ...
```

---

## 阶段四：参数化数据驱动

**目标**：把测试数据从代码中抽离，实现一组逻辑多组数据。

- 学习 `@pytest.mark.parametrize`
- 参数可以是单参数，也可以是多参数元组
- 数据写在装饰器里，也可以从文件 / Excel / YAML 读取

**实践**：把 `test_local.py` 的登录多组账号密码改成参数化：

```python
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "123456", "欢迎 admin"),
    ("admin", "wrong", "密码错误"),
    ("", "123456", "用户名不能为空"),
])
def test_login(driver, username, password, expected):
    ...
```

---

## 阶段五：用例标记与组织

**目标**：按功能给用例分类，方便选择性执行。

- `@pytest.mark.smoke` 冒烟测试
- `@pytest.mark.login`、`@pytest.mark.alert` 等业务标记
- 在 `pytest.ini` 中注册标记，避免警告
- `pytest -m login` 只运行登录相关用例
- `@pytest.mark.skip` 跳过暂不需要执行的用例
- `@pytest.mark.xfail` 标记预期失败的用例

**实践**：给现有用例打上 `login`、`select`、`checkbox`、`table`、`wait`、`alert` 等标记。

---

## 阶段六：Page Object 设计模式

**目标**：让元素定位和业务操作分离，提高可维护性。

- 在 `pages/` 目录下为每个页面创建 Python 类
- 页面类里封装元素定位器和操作方法
- 测试函数只负责调用页面类方法和写断言
- 定位器变更时只需改页面类，不用改测试

**实践示例**：

- `pages/login_page.py`：封装 `LoginPage` 类
- `pages/select_page.py`：封装下拉框操作
- `pages/table_page.py`：封装表格读取方法

测试里写成：

```python
def test_login(driver):
    page = LoginPage(driver)
    page.open()
    page.login("admin", "123456")
    assert page.welcome_text == "欢迎 admin"
```

---

## 阶段七：测试报告与工程化

**目标**：让测试结果可视化、可集成。

- `pytest-html` 生成 HTML 报告：`pytest --html=report.html`
- `Allure` 生成更美观的测试报告
- `pytest-xdist` 并发执行：`pytest -n auto`
- `pytest-rerunfailures` 失败用例自动重跑
- GitHub Actions / CI 自动运行测试

---

## 阶段八：扩展方向

**目标**：从 Web UI 测试延伸到其他测试领域。

- 接口自动化：`requests + pytest`
- 游戏测试：`Airtest + Poco`
- 移动端测试：`Appium + pytest`

---

## 推荐学习顺序

```
安装 pytest → 改写一个脚本 → 全部脚本 pytest 化
        ↓
Fixture 管理 driver → conftest.py 共享
        ↓
参数化数据驱动 → 登录表单多组数据
        ↓
用例标记分类 → pytest -m 筛选运行
        ↓
Page Object 重构 → pages/ 与 tests/ 分离
        ↓
接入 pytest-html / Allure 报告
        ↓
CI/CD 自动运行
```

> 💡 建议先完成前两个阶段，让现有 9 个脚本全部能在 pytest 下跑通并输出绿色通过，再逐步加入 Fixture、参数化和 Page Object。
