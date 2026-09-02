# 阶段五：高级 Selenium 操作

> 处理复杂 Web 交互，提升脚本稳定性。

---

## 1. JavaScript 执行

### 1.1 为什么要执行 JavaScript

有些场景用 Selenium 直接操作不方便：

- 元素被遮挡，无法正常点击
- 需要滚动页面才能看到元素
- 元素是只读的，无法直接输入
- 需要获取页面级信息

### 1.2 基本语法

```python
driver.execute_script("JavaScript 代码", 参数1, 参数2, ...)
```

### 1.3 常用场景

#### 滚动到元素

```python
element = driver.find_element(By.ID, "someId")
driver.execute_script("arguments[0].scrollIntoView();", element)
```

#### 移除只读属性

```python
element = driver.find_element(By.ID, "readonlyInput")
driver.execute_script("arguments[0].removeAttribute('readonly');", element)
element.send_keys("2026-08-31")
```

#### 强制点击

```python
element = driver.find_element(By.ID, "someId")
driver.execute_script("arguments[0].click();", element)
```

---

## 2. 高级等待策略

### 2.1 元素可点击

```python
wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.ID, "clickableBtn")))
```

### 2.2 元素可见

```python
wait = WebDriverWait(driver, 10)
box = wait.until(EC.visibility_of_element_located((By.ID, "visibleBox")))
```

### 2.3 元素出现在 DOM 中

```python
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "newDynamicElement")))
```

### 2.4 文本出现

```python
wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.ID, "dynamicText"), "✅ 文本已改变"))
```

### 2.5 元素消失

```python
wait = WebDriverWait(driver, 10)
wait.until(EC.invisibility_of_element_located((By.ID, "disappearBox")))
```

---

## 3. ActionChains 复杂操作

### 3.1 鼠标悬停

```python
from selenium.webdriver.common.action_chains import ActionChains

menu = driver.find_element(By.ID, "hoverMenu")
ActionChains(driver).move_to_element(menu).perform()
```

### 3.2 拖拽

```python
source = driver.find_element(By.ID, "dragSource")
target = driver.find_element(By.ID, "dragTarget")
ActionChains(driver).drag_and_drop(source, target).perform()
```

### 3.3 双击

```python
element = driver.find_element(By.ID, "doubleClickArea")
ActionChains(driver).double_click(element).perform()
```

### 3.4 右键点击

```python
element = driver.find_element(By.ID, "contextMenuArea")
ActionChains(driver).context_click(element).perform()
```

---

## 4. Frame 切换

### 4.1 切换到 iframe

```python
iframe = driver.find_element(By.ID, "innerFrame")
driver.switch_to.frame(iframe)
```

### 4.2 切回主页面

```python
driver.switch_to.default_content()
```

---

## 5. 窗口切换

### 5.1 获取所有窗口

```python
windows = driver.window_handles
```

### 5.2 切换到新窗口

```python
driver.switch_to.window(windows[-1])
```

### 5.3 关闭新窗口并切回

```python
driver.close()
driver.switch_to.window(windows[0])
```

---

## 6. 练习页面

本项目提供了专门的高级练习页面：

- [pages/advanced-practice.html](pages/advanced-practice.html)：主练习页面
- [pages/iframe-form.html](pages/iframe-form.html)：iframe 内嵌页面
- [pages/new-window.html](pages/new-window.html)：新窗口页面

对应 Page Object：[pages/advanced_page.py](pages/advanced_page.py)

对应测试文件：[tests_pytest/test_advanced_pytest.py](tests_pytest/test_advanced_pytest.py)

---

## 7. 注意事项

- `execute_script` 可以处理 Selenium 直接操作失败的场景，但不要过度依赖
- 等待时优先用显式等待，避免固定 `time.sleep()`
- 操作完 iframe 后记得切回主页面
- 操作完新窗口后记得切回原窗口

---

> 💡 学习建议：高级 Selenium 操作不是炫技，而是为了解决普通定位点击搞不定的问题。遇到问题时，先想能不能用显式等待解决，再考虑 JS 或 ActionChains。
