from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time


driver = webdriver.Edge()
# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")


#7.1点击“显示欢迎消息”按钮
showMessage_Btn = driver.find_element(By.ID,"showMessageBtn")
showMessage_Btn.click()

messageDisplay_content = driver.find_element(By.ID,'messageDisplay')
assert messageDisplay_content.text == '🎉 欢迎来到 Selenium 练习场！',"按钮未按下"
print(messageDisplay_content.text)

#7.2获取 #messageDisplay 的 class 属性
class_value = messageDisplay_content.get_attribute("class")
assert class_value == "success","获取属性失败"
print(class_value)

#7.3再次点击按钮，验证消息是否重复显示
showMessage_Btn.click()
assert messageDisplay_content.text == '🎉 欢迎来到 Selenium 练习场！',"按钮按下后未重复显示"
print(messageDisplay_content.text)



time.sleep(3)
driver.quit()

