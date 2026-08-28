from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import time

driver = webdriver.Edge()

# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

#3.1选择“女”单选按钮
female_radio = driver.find_element(By.ID,"female")
female_radio.click()

is_checked = female_radio.is_selected()
assert is_checked,"女单选按钮未被选中"
print("选中女单选按钮")

#3.2取消选中“邮件”复选框
email_checkbox = driver.find_element(By.ID,"emailNotify")
email_checkbox.click()

is_checked = email_checkbox.is_selected()
assert not is_checked,"邮件复选框未取消选中"
print("取消选中邮件复选框按钮")

#3.3选中“短信”复选框
sms_checkbox = driver.find_element(By.ID,"smsNotify")
sms_checkbox.click()

is_checked = sms_checkbox.is_selected()
assert is_checked,"未选中短信复选框"
print("选中短信复选框")

#3.4 验证“微信”复选框默认未选中
wechat_checkbox = driver.find_element(By.ID,"wechatNotify")

is_checked = wechat_checkbox.is_selected()
assert not is_checked,"微信复选框默认选中"
print("微信复选框默认未选中")

#3.5 点击微信复选框再次确认
wechat_checkbox.click()
is_checked = wechat_checkbox.is_selected()
assert is_checked,"微信复选框未被选中"
print("微信复选框已选中")

time.sleep(3)
driver.quit()