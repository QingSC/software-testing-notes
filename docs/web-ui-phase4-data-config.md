# 阶段四：测试数据与配置分离

> 让代码、数据、配置各司其职，方便维护和多环境切换。

---

## 1. 为什么需要分离

原来测试数据、页面地址、浏览器类型都直接写在代码里。这样有几个问题：

- 改测试数据要改代码
- 换环境要改多处代码
- 代码和配置混在一起，不好维护

分离后：

- 数据放在 YAML/JSON 文件
- 配置放在 JSON 文件
- 代码只负责业务逻辑

---

## 2. 数据分离：YAML

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

---

## 3. 配置分离：JSON

创建 `config/dev.json` 和 `config/test.json`：

```json
{
  "browser": "edge",
  "base_url": "../pages/practice.html"
}
```

---

## 4. 支持命令行选择环境

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

---

## 5. driver fixture 使用配置

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

---

## 6. Page Object 使用配置

```python
def open(self):
    file_path = self.driver.config.get("base_url")
    self.driver.logger.info(f"打开页面：{file_path}")
    self.driver.get(f"file:///{file_path}")
```

---

## 7. 运行方式

```bash
pytest                  # 默认使用 dev 环境
pytest --env=test      # 使用 test 环境
pytest --env=dev       # 使用 dev 环境
```

---

## 8. 注意事项

- YAML 里的数字密码要加引号，避免被解析成数字
- JSON 文件里不能写注释
- 配置文件也不要提交到 Git（如果包含敏感信息）
- `pytest_addoption` 是 pytest 固定名字的钩子函数

---

> 💡 学习建议：数据和配置分离后，测试代码会更干净。但不要把所有东西都抽到配置文件里，只有会变化的内容才适合放到配置中。
