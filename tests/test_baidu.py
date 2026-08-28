from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

# 1. 指定 Edge 驱动路径

driver = webdriver.Edge()

# 2. 打开百度首页
driver.get("https://www.baidu.com")

#3. 等待搜索框可交互 → 输入“软件测试”
wait = WebDriverWait(driver , 10)
search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))

# 用 JavaScript 强行设置值
driver.execute_script("arguments[0].value = '软件测试';", search_input)

# 打印一下值，确认是否写入成功
print("输入框当前值：", search_input.get_attribute("value"))

# 4. 等待搜索按钮可点击 → 点击
search_btn = wait.until(EC.element_to_be_clickable((By.XPATH,'//input[@value="百度一下"]')))
search_btn.click()

# 6. 打印成功信息
print("搜索成功!")

# 7. 等待3秒，让你看到搜索结果（可选）


time.sleep(3)

driver.quit()