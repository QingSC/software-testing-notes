# Software Testing Notes

这是一个软件测试学习笔记项目，主要使用 **Python + Selenium + pytest** 进行 Web 自动化测试练习。

项目记录了我从零散的 Selenium 脚本，逐步学习并重构为 **pytest + fixture + 参数化 + Page Object** 的过程。

---

## 📁 目录结构

```text
software-testing-notes/
├── pages/                      # 本地 HTML 练习页面
│   ├── practice.html           # 综合练习页面（登录、下拉框、弹窗、表格等）
│   └── test_local.html         # 早期简单练习页面
│
├── pages/                      # Page Object 封装类（与 HTML 页面同名目录）
│   ├── base_page.py            # 所有页面类的基类
│   ├── login_page.py           # 登录页封装
│   ├── select_page.py          # 下拉框封装
│   ├── radio_checkbox_page.py  # 单选/复选框封装
│   ├── textarea_page.py        # 文本域与动态内容封装
│   ├── table_page.py           # 表格封装
│   ├── wait_page.py            # 显式等待封装
│   ├── message_page.py         # 消息显示封装
│   └── alert_page.py           # Alert/Confirm 弹窗封装
│
├── tests/                      # 早期原始 Selenium 脚本（保留作为学习曲线）
│   ├── test_baidu.py           # 百度搜索（XPath + JS 输入）
│   ├── test_baidu_copy.py      # 百度搜索（多种定位方式兜底）
│   ├── test_local.py           # 登录表单多组数据断言
│   ├── text_local_2.py         # Select 下拉框与多选
│   ├── text_local_3.py         # 单选按钮与复选框
│   ├── text_local_4.py         # 文本域、动态内容、显示/隐藏
│   ├── text_local_5.py         # 表格数据遍历
│   ├── text_local_6.py         # 显式等待
│   ├── text_local_7.py         # 交互反馈与属性获取
│   └── text_local_8.py         # Alert / Confirm 弹窗
│
├── tests_pytest/               # pytest 重构后的测试（推荐从这里开始看）
│   ├── conftest.py             # driver / practice_page fixture
│   ├── test_login_pytest.py    # 登录 + 参数化
│   ├── test_select_pytest.py
│   ├── test_radio_checkbox_pytest.py
│   ├── test_textarea_dynamic_pytest.py
│   ├── test_table_pytest.py
│   ├── test_wait_pytest.py
│   ├── test_message_pytest.py
│   └── test_alert_pytest.py
│
├── docs/                       # 学习笔记
│   ├── pytest-notes.md         # pytest 常用语法速查
│   ├── pytest-learning-guide.md # pytest 学习路线图
│   └── selenium-basics-notes.md # Selenium 基础语法笔记
│
├── Driver_Notes/               # Edge WebDriver 自带文档
├── pytest.ini                  # pytest 配置（markers / testpaths）
├── requirements.txt            # Python 依赖
├── .gitignore
└── README.md
```

> 💡 `tests/` 目录里的脚本是学习初期的原始写法，保留下来展示从“原始脚本”到“pytest 工程化”的演进过程。

---

## 🛠️ 环境要求

- Python 3.9+
- Microsoft Edge 浏览器
- Edge WebDriver（推荐让 `webdriver-manager` 自动管理）

---

## 🚀 快速开始

### 1. 创建并激活虚拟环境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行 pytest 测试

```bash
# 运行所有 pytest 测试
pytest

# 详细输出
pytest -v

# 显示 print() 内容
pytest -s

# 按标记运行
pytest -m login
pytest -m smoke

# 生成 HTML 报告
pytest --html=report.html --self-contained-html
```

### 4. 运行单个旧脚本（可选）

```bash
cd tests
python text_local_8.py
```

---

## 📚 学习内容

### 本地练习页面覆盖的测试场景

| 练习主题 | 原始脚本 | pytest 版本 | Page Object |
|---|---|---|---|
| 登录表单数据驱动 | `test_local.py` | `test_login_pytest.py` | `login_page.py` |
| Select 下拉框与多选 | `text_local_2.py` | `test_select_pytest.py` | `select_page.py` |
| 单选按钮与复选框 | `text_local_3.py` | `test_radio_checkbox_pytest.py` | `radio_checkbox_page.py` |
| 文本域、动态内容、显示/隐藏 | `text_local_4.py` | `test_textarea_dynamic_pytest.py` | `textarea_page.py` |
| 表格数据遍历 | `text_local_5.py` | `test_table_pytest.py` | `table_page.py` |
| 显式等待与延迟加载 | `text_local_6.py` | `test_wait_pytest.py` | `wait_page.py` |
| 交互反馈与属性获取 | `text_local_7.py` | `test_message_pytest.py` | `message_page.py` |
| Alert / Confirm 弹窗 | `text_local_8.py` | `test_alert_pytest.py` | `alert_page.py` |

### 学习笔记

| 笔记 | 内容 |
|---|---|
| [docs/selenium-basics-notes.md](docs/selenium-basics-notes.md) | Selenium 基础语法：定位、操作、断言、弹窗、等待 |
| [docs/pytest-notes.md](docs/pytest-notes.md) | pytest 速查：fixture、参数化、markers、报告、并行 |
| [docs/pytest-learning-guide.md](docs/pytest-learning-guide.md) | 从原始脚本到 pytest 工程化的学习路线图 |

---

## ✅ 已掌握的技能

- [x] Selenium 基础元素定位与操作
- [x] `assert` 断言替代 `print` 判断
- [x] pytest 测试发现与运行
- [x] `@pytest.fixture` 管理 WebDriver
- [x] `@pytest.mark.parametrize` 数据驱动
- [x] `@pytest.mark` 用例分类与筛选
- [x] Page Object 设计模式
- [x] pytest-html 生成测试报告

## 🔜 后续学习计划

- [ ] 接入 Allure 测试报告
- [ ] 失败用例自动重跑（pytest-rerunfailures）
- [ ] 并行执行测试（pytest-xdist）
- [ ] GitHub Actions CI 自动运行测试
- [ ] 接口自动化测试（requests + pytest）
- [ ] 游戏测试探索（Airtest + Poco）

---

## 📝 说明

- `msedgedriver.exe` 和 `edgedriver_win64.zip` 为本地运行所需，未提交到 Git。
- `venv/` 为 Python 虚拟环境，未提交到 Git。
- `report.html` 为本地生成的测试报告，未提交到 Git。

---

> 💡 建议学习顺序：先读 [docs/selenium-basics-notes.md](docs/selenium-basics-notes.md) 理解原始脚本 → 再读 [docs/pytest-notes.md](docs/pytest-notes.md) 理解重构后的写法 → 最后看 [docs/pytest-learning-guide.md](docs/pytest-learning-guide.md) 规划进阶方向。
