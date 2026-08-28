from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import time

driver = webdriver.Edge()

# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

#2.1
city_select = Select(driver.find_element(By.ID,"citySelect"))

city_select.select_by_value("shenzhen")

selected = city_select.first_selected_option

assert selected.text == '深圳',f'失败，预期为深圳，实际为{selected.text}'

print(selected.text)

#2.2
hobby_select = Select(driver.find_element(By.ID,"hobbySelect"))
hobby_select.select_by_value("coding")
hobby_select.select_by_value("sports")

all_selected = hobby_select.all_selected_options
for option in all_selected:
    assert option.text in ["编程", "运动"],f"勾选的属性不在编程和运动内"
    print(option.text)

#2.3
city_select.select_by_value("guangzhou")
selected = city_select.first_selected_option
assert selected.text == '广州',f'失败，预期为广州，实际为{selected.text}'
print(selected.text)

#2.4
hobby_select.deselect_by_value("coding")

all_selected = hobby_select.all_selected_options
for option in all_selected:
    assert option.text in "运动",f"未能取消勾选编程选项"
    print(option.text)

time.sleep(3)
driver.quit()