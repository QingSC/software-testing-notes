from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from datetime import datetime
import os
import time


driver = webdriver.Edge()
wait = WebDriverWait(driver,10)
# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

#8.1点击"弹出 Alert"按钮
alert_Btn = driver.find_element(By.ID,"alertBtn")
alert_Btn.click()

# 点击按钮后，弹窗出现
wait.until(EC.alert_is_present())
alert = Alert(driver)
# 获取弹窗中的文字
alert_text = alert.text
assert alert_text == '这是一个 Alert 弹窗！' ,"未获取到到Alert 弹窗文字"
print(alert_text)
# 点击"确定"
alert.accept()

#8.2点击"弹出 Confirm"按钮
confirm_Btn = driver.find_element(By.ID,"confirmBtn")
confirm_Btn.click()
wait.until(EC.alert_is_present())
#切换到Confirm弹窗，点击确定
confirm = Alert(driver)
alert.accept()

confirmResult_content = driver.find_element(By.ID,"confirmResult")
assert confirmResult_content.text == "✅ 你点击了“确定”"
print(confirmResult_content.text)

#8.3再次点击"弹出 Confirm"按钮
confirm_Btn.click()
wait.until(EC.alert_is_present())
#切换到Confirm弹窗，点击取消
confirm = Alert(driver)
confirm.dismiss()

confirmResult_content = driver.find_element(By.ID,"confirmResult")
assert confirmResult_content.text == "❌ 你点击了“取消”"
print(confirmResult_content.text)

time.sleep(3)
driver.quit()



