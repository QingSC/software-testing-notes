from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Edge()

# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

#4.1修改文本域内容为“自动化测试练习”
# 定位文本域
comment_textarea = driver.find_element(By.ID,"comment")
# 清空并输入新内容
comment_textarea.clear()
comment_textarea.send_keys("自动化测试练习")

# 获取文本域的值
comment_value = comment_textarea.get_attribute("value")
assert comment_value == "自动化测试练习",f"内容不符：{comment_value}"
print(comment_value)

#4.2点击“更新内容”按钮
update_Btn = driver.find_element(By.ID,"updateBtn")
update_Btn.click()

# 获取元素的文本内容
dynamic_content = driver.find_element(By.ID,"dynamic-content")
text = dynamic_content.text
assert "自动化测试练习" in text,"文本不包含'自动化测试练习'"
print(text)

#4.3点击“显示隐藏区域”按钮
showhidden_Btn = driver.find_element(By.ID,"showHiddenBtn")
showhidden_Btn.click()

hidden_content = driver.find_element(By.ID,"hiddenDiv")
# 判断元素是否可见（返回 True / False）
is_visible = hidden_content.is_displayed()
assert is_visible,"隐藏元素不可见"
print("隐藏元素可见")

#4.4再次点击“显示隐藏区域”按钮
showhidden_Btn.click()
is_visible = hidden_content.is_displayed()
assert not is_visible,"元素未被隐藏"
print("元素变为隐藏")


time.sleep(3)
driver.quit()