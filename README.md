# Software Testing Notes

这是一个软件测试学习笔记项目，主要使用 Python + Selenium + Edge WebDriver 进行 Web 自动化测试练习。

## 📁 目录结构

```
software-testing-notes/
├── pages/                  # HTML 练习页面
│   ├── practice.html       # Selenium 综合练习页面
│   └── test_local.html     # 简单本地测试页面
├── tests/                  # Python 测试脚本
│   ├── test_baidu.py
│   ├── test_baidu_copy.py
│   ├── test_local.py
│   ├── text_local_2.py     # 下拉框与多选
│   ├── text_local_3.py     # 单选与复选框
│   ├── text_local_4.py     # 文本域与动态内容
│   ├── text_local_5.py     # 表格数据
│   ├── text_local_6.py     # 显式等待
│   ├── text_local_7.py     # 交互反馈
│   └── text_local_8.py     # Alert/Confirm 弹窗
├── Driver_Notes/           # Edge WebDriver 文档
├── .gitignore
├── README.md
└── requirements.txt
```

## 🛠️ 环境要求

- Python 3.9+
- Microsoft Edge 浏览器
- Edge WebDriver (`msedgedriver.exe`)

## 🚀 快速开始

1. 创建并激活虚拟环境：

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 运行测试脚本：

```bash
cd tests
python text_local_8.py
```

## 📚 学习内容

| 脚本 | 练习主题 |
|------|---------|
| test_local.py | 登录表单数据驱动测试 |
| text_local_2.py | Select 下拉框与多选 |
| text_local_3.py | 单选按钮与复选框 |
| text_local_4.py | 文本域、动态内容、显示/隐藏 |
| text_local_5.py | 表格数据遍历与断言 |
| text_local_6.py | 显式等待与延迟加载 |
| text_local_7.py | 交互反馈与属性获取 |
| text_local_8.py | Alert / Confirm 弹窗处理 |

## 📝 说明

- `msedgedriver.exe` 和 `edgedriver_win64.zip` 为本地运行所需，未提交到 Git。
- `venv/` 为 Python 虚拟环境，未提交到 Git。

## 🔜 后续计划

- [ ] 用 pytest 重构测试脚本
- [ ] 引入 Page Object 设计模式
- [ ] 接入 Allure 测试报告
- [ ] 学习接口自动化测试（requests + pytest）
- [ ] 探索游戏测试方向（Airtest + Poco）
