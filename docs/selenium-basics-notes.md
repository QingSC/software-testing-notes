# Selenium 基础测试语法笔记

> 根据 `tests/` 目录里的练习脚本整理，记录 Selenium Web 自动化测试最基础、最常用的语法。

---

## 1. 创建和关闭浏览器

```python
from selenium import webdriver

# 创建 Edge 浏览器对象
# 如果 msedgedriver.exe 已经加入系统环境变量，可以直接这样写
driver = webdriver.Edge()

# 如果驱动文件放在项目根目录，需要手动指定路径
from selenium.webdriver.edge.service import Service
service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)

# 最大化窗口
driver.maximize_window()

# 测试结束后关闭浏览器
driver.quit()
```

---

## 2. 打开网页

```python
# 打开百度首页
driver.get("https://www.baidu.com")

# 打开本地练习页面
import os
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")
```

`os.path.abspath()` 把相对路径转成绝对路径，避免不同目录下运行时找不到文件。

---

## 3. 元素定位

需要先导入 `By`：

```python
from selenium.webdriver.common.by import By
```

### 3.1 按 ID 定位

```python
element = driver.find_element(By.ID, "username")
```

### 3.2 按 Name 定位

```python
element = driver.find_element(By.NAME, "wd")
```

### 3.3 按 XPath 定位

```python
element = driver.find_element(By.XPATH, '//input[@type="text"]')
```

### 3.4 按 Tag 名称定位

```python
elements = driver.find_elements(By.TAG_NAME, "tr")
```

### 3.5 查找子元素

```python
table = driver.find_element(By.ID, "dataTable")
rows = table.find_elements(By.TAG_NAME, "tr")
```

`find_element` 返回单个元素，`find_elements` 返回元素列表。

---

## 4. 元素基本操作

### 4.1 输入内容

```python
username_input = driver.find_element(By.ID, "username")
username_input.clear()                    # 先清空
username_input.send_keys("admin")         # 再输入
```

### 4.2 点击元素

```python
login_btn = driver.find_element(By.ID, "loginBtn")
login_btn.click()
```

### 4.3 获取元素文本

```python
result = driver.find_element(By.ID, "loginResult").text
```

### 4.4 获取元素属性

```python
value = driver.find_element(By.ID, "comment").get_attribute("value")
class_value = driver.find_element(By.ID, "messageDisplay").get_attribute("class")
```

### 4.5 用键盘按键提交

```python
from selenium.webdriver.common.keys import Keys
search_box.send_keys("软件测试" + Keys.RETURN)
```

### 4.6 用 JavaScript 操作元素

当普通方法无法输入或点击时，可以用 JS 强制执行：

```python
search_input = driver.find_element(By.XPATH, '//input[@type="text"]')
driver.execute_script("arguments[0].value = '软件测试';", search_input)
driver.execute_script("document.getElementById('su').click();")
```

---

## 5. 断言 assert

pytest 和原生 Python 脚本里都可以直接用 `assert`。

```python
# 判断相等
assert 1 + 1 == 2

# 判断包含
result = driver.find_element(By.ID, "loginResult").text
assert "登录成功" in result

# 判断为真
radio = driver.find_element(By.ID, "female")
assert radio.is_selected(), "女单选按钮未被选中"

# 判断为假
email = driver.find_element(By.ID, "emailNotify")
assert not email.is_selected(), "邮件复选框未取消选中"

# 带自定义错误信息
city = cells[2].text
assert city == "上海", f"查询到李四所在城市不是上海，而是 {city}"
```

如果断言失败，程序会抛出 `AssertionError` 并停止运行。

---

## 6. 单选按钮和复选框

### 6.1 判断元素是否被选中

```python
radio = driver.find_element(By.ID, "female")
radio.click()

is_checked = radio.is_selected()
assert is_checked, "女单选按钮未被选中"
```

### 6.2 判断元素是否可见

```python
hidden = driver.find_element(By.ID, "hiddenDiv")
visible = hidden.is_displayed()
assert visible, "隐藏元素不可见"
```

---

## 7. Select 下拉框

需要先导入 `Select`：

```python
from selenium.webdriver.support.ui import Select
```

### 7.1 单选下拉框

```python
city_select = Select(driver.find_element(By.ID, "citySelect"))
city_select.select_by_value("shenzhen")

selected = city_select.first_selected_option
assert selected.text == "深圳"
```

### 7.2 多选下拉框

```python
hobby_select = Select(driver.find_element(By.ID, "hobbySelect"))
hobby_select.select_by_value("coding")
hobby_select.select_by_value("sports")

# 获取所有已选项
all_selected = hobby_select.all_selected_options
for option in all_selected:
    print(option.text)
```

### 7.3 取消选中

```python
hobby_select.deselect_by_value("coding")
```

---

## 8. 表格操作

```python
table = driver.find_element(By.ID, "dataTable")
rows = table.find_elements(By.TAG_NAME, "tr")

# 判断表格行数
assert len(rows) == 4, "总行数不为 4 行"

# 遍历每一行，查找指定姓名的城市
for row in rows[1:]:                       # 跳过表头
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0 and cells[0].text == "李四":
        city = cells[2].text
        assert city == "上海"
```

---

## 9. 显式等待

页面元素不会立刻出现时，需要等待。

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 最多等待 10 秒
wait = WebDriverWait(driver, 10)

# 等待元素可点击
search_box = wait.until(
    EC.element_to_be_clickable((By.ID, "kw"))
)

# 等待元素出现在 DOM 中
search_input = wait.until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
)

# 等待元素中出现指定文本
wait.until(
    EC.text_to_be_present_in_element((By.ID, "delayedContent"), "数据加载完成")
)

# 等待弹窗出现
wait.until(EC.alert_is_present())
```

---

## 10. Alert 和 Confirm 弹窗

```python
from selenium.webdriver.common.alert import Alert

# 点击按钮弹出 Alert
alert_btn = driver.find_element(By.ID, "alertBtn")
alert_btn.click()

# 切换到弹窗
alert = Alert(driver)

# 获取弹窗文字
alert_text = alert.text
assert alert_text == "这是一个 Alert 弹窗！"

# 点击确定
alert.accept()

# 如果是 Confirm 弹窗，还可以点击取消
confirm = Alert(driver)
confirm.dismiss()
```

---

## 11. 常用断言技巧

| 场景 | 写法 |
|---|---|
| 文本相等 | `assert text == "预期文本"` |
| 文本包含 | `assert "预期" in text` |
| 列表包含 | `assert name in ["张三", "李四"]` |
| 元素已选中 | `assert element.is_selected()` |
| 元素未选中 | `assert not element.is_selected()` |
| 元素可见 | `assert element.is_displayed()` |
| 元素不可见 | `assert not element.is_displayed()` |
| 行数判断 | `assert len(rows) == 4` |

---

## 12. 一个完整的登录测试脚本示例

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# 1. 创建浏览器
driver = webdriver.Edge()

# 2. 打开本地练习页面
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

# 3. 测试数据
test_data = [
    ("admin", "123456", "登录成功"),
    ("", "123456", "请输入用户名"),
    ("admin", "", "请输入密码"),
]

# 4. 遍历每组数据执行测试
for user, pwd, expected in test_data:
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.ID, "loginBtn")

    username_input.clear()
    username_input.send_keys(user)
    password_input.clear()
    password_input.send_keys(pwd)
    login_btn.click()

    result = driver.find_element(By.ID, "loginResult").text
    assert expected in result, f"测试失败！预期包含 '{expected}'，实际为 '{result}'"

    time.sleep(0.5)

# 5. 关闭浏览器
driver.quit()
```

---

## 13. `tests/` 目录练习对应表

| 脚本 | 练习内容 |
|---|---|
| `test_baidu.py` | 百度搜索 + XPath + JavaScript 输入 |
| `test_baidu_copy.py` | 多种定位方式兜底 + 显式等待 |
| `test_local.py` | 本地登录表单 + 多组数据 + assert |
| `text_local_2.py` | Select 单选/多选/取消选择 |
| `text_local_3.py` | 单选按钮 / 复选框状态断言 |
| `text_local_4.py` | 文本域、动态内容、隐藏区域可见性 |
| `text_local_5.py` | 表格读取、行数断言、列数据断言 |
| `text_local_6.py` | 显式等待 + 加载状态断言 |
| `text_local_7.py` | 交互反馈文本 + class 属性断言 |
| `text_local_8.py` | Alert / Confirm 弹窗处理 |

---

> 💡 学习建议：先把这 9 个脚本跑通，理解每个定位方式和断言，再去看 `docs/pytest-notes.md` 学习如何用 pytest 重构它们。
