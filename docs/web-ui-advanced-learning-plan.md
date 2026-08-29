# Web UI 自动化测试深化学习计划

> 基于本项目当前进度制定的进阶路线，目标是从"能写脚本"成长为"能搭框架、能持续集成"的测试工程师。

---

## 计划评审说明

### 当前基础（已具备）

- Selenium 基础元素定位与操作
- `assert` 断言
- pytest 测试发现与运行
- `@pytest.fixture` 管理 WebDriver
- `@pytest.mark.parametrize` 数据驱动
- `@pytest.mark` 用例分类
- Page Object 设计模式
- pytest-html 报告
- pytest-xdist 并行执行

### 原计划的优点

1. **由浅入深**：从报告美化到框架设计，难度递增合理
2. **贴近工程实践**：覆盖了失败重试、数据分离、CI/CD 等真实工作场景
3. **有明确产出**：每个阶段都有可交付的内容
4. **技术栈主流**：Allure、requests、GitHub Actions 都是行业常用工具

### 原计划需要改进的地方

1. **缺少测试理论基础**：自动化不是只写代码，测试用例设计方法很重要
2. **报告阶段顺序偏早**：建议先学会失败截图和日志，再学 Allure 报告，这样报告才有内容可展示
3. **缺少环境管理**：不同环境（开发/测试/生产）的配置切换没提到
4. **缺少测试数据策略**：数据清理、数据隔离、数据库断言应该补充
5. **时间估算偏乐观**：初学者每个阶段可能需要更多时间消化
6. **缺少里程碑检查点**：应该设置阶段验收标准
7. **缺少学习资源推荐**：每个阶段应该配文档/视频

### 改进后的核心思路

```text
测试理论补充 → 失败诊断能力 → 数据与配置管理 → 高级操作 → 多环境多浏览器
        ↓
接口自动化扩展 → 框架设计 → CI/CD 持续集成 → 作品集项目
```

---

## 前置基础检查

在开始学习前，确保以下检查项都已完成：

- [ ] `pytest -v` 能在本项目跑通全部 27 个用例
- [ ] 能解释 `conftest.py` 中 `driver` fixture 的作用
- [ ] 能解释 `@pytest.mark.parametrize` 的用法
- [ ] 能解释 `pytestmark` 的用法
- [ ] 能解释 Page Object 为什么要分层
- [ ] 能用 Git 正常提交和推送代码

如果还有没完成的，先回到基础阶段补完。

---

## 阶段一：测试理论与用例设计（1 周）

### 目标

建立测试思维，不只是写代码，而是设计有效的测试。

### 学习内容

1. **测试基本原则**
   - 测试是为了发现缺陷，而不是证明没有缺陷
   - 不可能 100% 测试覆盖
   - 尽早测试、持续测试

2. **黑盒测试用例设计方法**
   - 等价类划分
   - 边界值分析
   - 判定表驱动法
   - 错误推测法
   - 场景法

3. **测试用例要素**
   - 用例编号
   - 测试标题
   - 前置条件
   - 测试步骤
   - 预期结果
   - 优先级

4. **Web 测试常见测试点**
   - 功能测试
   - 兼容性测试（浏览器、分辨率）
   - 性能测试（加载速度）
   - 安全性测试（XSS、SQL 注入基础）
   - 易用性测试

### 实践任务

为本项目 `pages/practice.html` 页面写一份手工测试用例文档，至少包含 15 条用例，覆盖登录、下拉框、单选/复选、表格、弹窗等模块。

### 产出

- `docs/manual-test-cases.md` 手工测试用例文档

### 推荐资源

- 《软件测试》（朱少民）第 3-5 章
- B 站搜"等价类划分 边界值分析"

---

## 阶段二：失败诊断能力（1-2 周）

### 目标

测试失败时，能快速定位问题原因。

### 学习内容

1. **pytest 失败信息阅读**
   - 如何看懂 `AssertionError`
   - 如何定位失败行号
   - `pytest -l` 显示局部变量

2. **失败自动截图**
   - `pytest_runtest_makereport` 钩子函数
   - `driver.save_screenshot()`
   - 按用例名保存截图

3. **日志记录**
   - Python `logging` 模块
   - 配置日志级别（DEBUG/INFO/ERROR）
   - 在关键步骤记录日志

4. **失败重试**
   - `pytest-rerunfailures` 插件
   - 配置重试次数和间隔
   - 理解什么时候该重试，什么时候不该重试

### 实践任务

1. 在 [tests_pytest/conftest.py](tests_pytest/conftest.py) 中实现失败自动截图
2. 配置日志输出到 `logs/` 目录
3. 在 [pytest.ini](pytest.ini) 中配置默认重试 2 次

### 产出

- `screenshots/` 目录，失败时自动生成截图
- `logs/` 目录，记录测试执行日志
- `pytest.ini` 配置重试策略

### 推荐资源

- pytest 官方文档 Hooks 章节
- Python `logging` 官方文档

---

## 阶段三：Allure 测试报告（3-5 天）

### 目标

生成专业、美观、信息量丰富的测试报告。

### 学习内容

1. **Allure 环境搭建**
   - 安装 `allure-pytest`
   - 安装 Allure Commandline
   - 生成并查看报告

2. **Allure 注解**
   - `@allure.feature` 功能模块
   - `@allure.story` 用户故事
   - `@allure.title` 用例标题
   - `@allure.step` 操作步骤
   - `@allure.severity` 严重程度
   - `@allure.attach` 添加附件（截图、日志）

3. **报告解读**
   - 总览页：通过/失败/跳过统计
   - 用例页：步骤、日志、附件
   - 图表页：执行时间分布

### 实践任务

为 `tests_pytest/` 下所有用例添加 Allure 注解，并集成失败截图附件。

### 产出

- 能生成并查看 Allure 报告
- 报告里包含用例标题、步骤、失败截图

### 推荐资源

- Allure 官方文档：https://docs.qameta.io/allure/
- B 站 Allure + pytest 教程

---

## 阶段四：测试数据与配置分离（1-2 周）

### 目标

让代码、数据、配置各司其职，方便维护和多环境切换。

### 学习内容

1. **YAML 管理测试数据**
   ```yaml
   # data/login_data.yaml
   login_cases:
     - username: admin
       password: "123456"
       expected: 登录成功
   ```

2. **JSON/INI 管理配置**
   ```json
   {
     "browser": "edge",
     "headless": false,
     "implicit_wait": 10,
     "explicit_wait": 10
   }
   ```

3. **环境配置管理**
   - 开发环境 dev
   - 测试环境 test
   - 生产环境 prod（谨慎使用）

4. **测试数据策略**
   - 数据与用例分离
   - 测试数据准备与清理
   - 避免测试数据互相污染

### 实践任务

1. 创建 `data/` 目录，把登录测试数据抽到 YAML 文件
2. 创建 `config/` 目录，管理环境和浏览器配置
3. 修改测试函数从文件读取数据

### 产出

- `data/login_data.yaml`
- `config/dev.json`、`config/test.json`
- 测试代码不再硬编码数据

### 推荐资源

- PyYAML 官方文档
- Python `configparser` 标准库

---

## 阶段五：高级 Selenium 操作（1-2 周）

### 目标

处理复杂 Web 交互，提升脚本稳定性。

### 学习内容

1. **ActionChains 复杂操作**
   - 鼠标悬停 `move_to_element`
   - 拖拽 `drag_and_drop`
   - 右键点击 `context_click`
   - 双击 `double_click`

2. **Frame 和窗口切换**
   - `driver.switch_to.frame()`
   - `driver.switch_to.default_content()`
   - `driver.switch_to.window()`
   - `driver.switch_to.alert`

3. **JavaScript 执行**
   - 滚动页面
   - 修改只读属性
   - 强制点击被遮挡元素

4. **高级等待策略**
   - 等待元素可见
   - 等待元素可点击
   - 等待元素消失
   - 自定义 expected condition

5. **弹窗处理**
   - Alert
   - Confirm
   - Prompt
   - 自定义模态框

### 实践任务

找一个带下拉菜单、iframe、弹窗、滚动加载的公开网站（如 Element UI 组件库），写一个综合测试脚本。

### 产出

- 至少掌握 3 种复杂交互
- 能处理 iframe 和新窗口

### 推荐资源

- Selenium with Python 官方文档
- Element UI 官方组件库（练习用）

---

## 阶段六：多浏览器与多环境支持（1 周）

### 目标

一套代码跑多个浏览器和多个环境。

### 学习内容

1. **webdriver-manager 自动管理驱动**
   ```bash
   pip install webdriver-manager
   ```

2. **命令行参数选择浏览器**
   ```bash
   pytest --browser=chrome
   pytest --browser=edge
   pytest --browser=firefox
   ```

3. **pytest 自定义命令行参数**
   - `pytest_addoption`
   - `parser.addoption`

4. **环境切换**
   ```bash
   pytest --env=test
   pytest --env=dev
   ```

### 实践任务

1. 修改 `conftest.py`，支持 `--browser` 和 `--env` 参数
2. 用 Chrome 和 Edge 各跑一遍全部用例

### 产出

```bash
pytest --browser=chrome --env=test
pytest --browser=edge --env=dev
```

### 推荐资源

- webdriver-manager 文档
- pytest 官方文档 Customizing pytest

---

## 阶段七：接口自动化测试（2-3 周）

### 目标

从 UI 层扩展到接口层，形成多层测试能力。

### 学习内容

1. **requests 基础**
   - GET / POST / PUT / DELETE
   - params / data / json / headers
   - 响应状态码、响应头、响应体
   - JSON 解析

2. **pytest + requests 组织用例**
   - 用 fixture 管理 session
   - 用 assert 校验响应
   - 接口参数化

3. **接口测试常见断言**
   - 状态码断言
   - 响应字段断言
   - 响应时间断言
   - JSON Schema 校验

4. **UI 与接口结合**
   - 接口准备测试数据
   - UI 验证页面表现
   - 接口清理测试数据

### 实践任务

1. 新建 `tests_api/` 目录
2. 用 JSONPlaceholder 或本项目本地接口写 5-10 个接口测试
3. 写一个"接口登录 + UI 验证"的联合测试

### 产出

- `tests_api/test_api_xxx.py`
- 至少一个 UI + 接口联合测试用例

### 推荐资源

- requests 官方文档
- JSONPlaceholder：https://jsonplaceholder.typicode.com/

---

## 阶段八：测试框架设计（2-3 周）

### 目标

从写用例进化到设计可维护的测试框架。

### 学习内容

1. **框架目录结构**
   ```text
   project/
   ├── config/           # 配置文件
   ├── data/             # 测试数据
   ├── pages/            # Page Object
   ├── tests/            # 测试用例
   ├── tests_api/        # 接口测试
   ├── utils/            # 工具类
   │   ├── logger.py
   │   ├── config_reader.py
   │   ├── data_reader.py
   │   └── screenshot_helper.py
   ├── reports/          # 报告输出
   ├── conftest.py
   ├── pytest.ini
   └── requirements.txt
   ```

2. **工具类封装**
   - 日志工具
   - 配置读取
   - 数据读取（YAML/Excel/JSON）
   - 截图工具
   - 邮件通知

3. **异常处理**
   - 自定义异常
   - 失败处理策略
   - 测试跳过与标记

4. **数据库断言（基础）**
   - 用 Python 连接 MySQL/SQLite
   - 执行查询并断言结果
   - 测试数据清理

### 实践任务

把当前项目按上面的目录结构重构一次。

### 产出

- 清晰的目录结构
- 可复用的工具类
- 配置、数据、代码完全分离

### 推荐资源

- PyMySQL / sqlite3 文档
- 优秀开源测试框架源码

---

## 阶段九：CI/CD 持续集成（1-2 周）

### 目标

让测试在代码提交后自动运行。

### 学习内容

1. **GitHub Actions 基础**
   - `.github/workflows/` 目录
   - 触发条件：`push`、`pull_request`
   - job、step、action 概念

2. **编写测试工作流**
   ```yaml
   name: Run Tests
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
         - run: pip install -r requirements.txt
         - run: pytest
   ```

3. **Allure 报告上传**
   - 生成 Allure 结果
   - 上传 artifact
   - 配置 GitHub Pages 展示报告（进阶）

4. **邮件/消息通知**
   - 测试失败发送邮件
   - 企业微信/钉钉/飞书通知

### 实践任务

为本项目添加 GitHub Actions，每次 push 自动跑 pytest 并生成 Allure 报告。

### 产出

- `.github/workflows/test.yml`
- 每次提交自动运行测试
- 可下载或在线查看 Allure 报告

### 推荐资源

- GitHub Actions 官方文档
- Allure GitHub Actions 插件

---

## 阶段十：作品集项目（持续）

### 目标

做出能写在简历里的完整项目。

### 推荐项目一：电商网站自动化测试

**范围**：
- 用户登录/注册
- 商品搜索
- 商品详情
- 购物车
- 下单流程

**技术栈**：
- pytest + Selenium
- Page Object
- Allure 报告
- GitHub Actions CI

### 推荐项目二：后台管理系统自动化测试

**范围**：
- 登录
- 用户管理 CRUD
- 角色权限
- 数据查询与导出

**技术栈**：
- pytest + Selenium
- 接口准备数据
- YAML 数据驱动
- 多浏览器支持

### 推荐项目三：UI + 接口联合测试

**范围**：
- 接口创建测试数据
- UI 验证页面展示
- 接口清理数据
- 生成完整报告

### 作品集要求

- [ ] 有完整的 README
- [ ] 有清晰的目录结构
- [ ] 有 Allure 或 HTML 报告示例
- [ ] 有 CI/CD 配置
- [ ] 有截图或录屏展示运行效果
- [ ] 代码规范、注释清晰

---

## 学习里程碑检查点

| 检查点 | 验收标准 |
|---|---|
| 阶段一完成 | 写出 15 条以上手工测试用例 |
| 阶段二完成 | 失败自动截图 + 日志 + 重试 |
| 阶段三完成 | 生成第一份 Allure 报告 |
| 阶段四完成 | 数据与配置完全分离 |
| 阶段五完成 | 能处理 iframe、弹窗、复杂交互 |
| 阶段六完成 | 支持 Chrome/Edge 切换 + 环境切换 |
| 阶段七完成 | 写出 5 个以上接口测试用例 |
| 阶段八完成 | 项目目录结构规范、工具类可复用 |
| 阶段九完成 | GitHub Actions 自动跑通测试 |
| 阶段十完成 | 产出 1 个完整作品集项目 |

---

## 学习时间规划

| 阶段 | 建议时间 | 每日投入 |
|---|---|---|
| 阶段一：测试理论 | 1 周 | 1 小时 |
| 阶段二：失败诊断 | 1-2 周 | 1-2 小时 |
| 阶段三：Allure 报告 | 3-5 天 | 1-2 小时 |
| 阶段四：数据与配置分离 | 1-2 周 | 1-2 小时 |
| 阶段五：高级 Selenium | 1-2 周 | 1-2 小时 |
| 阶段六：多浏览器多环境 | 1 周 | 1-2 小时 |
| 阶段七：接口自动化 | 2-3 周 | 1-2 小时 |
| 阶段八：框架设计 | 2-3 周 | 1-2 小时 |
| 阶段九：CI/CD | 1-2 周 | 1-2 小时 |
| 阶段十：作品集 | 持续 | 灵活安排 |

**总计约 3-4 个月**，具体取决于每天投入时间和理解速度。

---

## 学习建议

1. **不要跳阶段**：前面基础不牢，后面框架设计会很难受
2. **边学边做**：每个阶段必须有产出，不能只看不动手
3. **多复盘**：每完成一个阶段，回顾学到了什么
4. **保持输出**：把学习内容写成笔记或博客
5. **项目驱动**：尽量用真实项目或公开网站练手

---

## 与游戏测试方向的对比

| 维度 | Web UI 深化 | 游戏测试 |
|---|---|---|
| 岗位数量 | 多 | 较少 |
| 入行难度 | 较低 | 中等 |
| 技术通用性 | 高 | 中等 |
| 薪资天花板 | 高 | 高（进大厂） |
| 适合人群 | 想稳就业、打基础 | 热爱游戏、愿意钻研 |
| 学习周期 | 3-4 个月 | 4-6 个月 |

**建议**：先完成 Web UI 深化前 6 个阶段，具备独立工作能力后，再决定是否扩展游戏测试方向。

---

> 💡 下一步推荐：从 **阶段一：测试理论与用例设计** 开始，先为 `practice.html` 写一份手工测试用例文档。
