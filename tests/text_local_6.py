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

# 等待最多 10 秒，直到某个条件成立
wait = WebDriverWait(driver,10)

##6.1点击“点击加载数据”按钮
load_Btn = driver.find_element(By.ID,"loadBtn")
load_Btn.click()

delayed_Content = driver.find_element(By.ID,"delayedContent")
assert delayed_Content.text == "⏳ 加载中...","未成功点击加载按钮"

##6.2等待内容更新为“数据加载完成”
wait.until(EC.text_to_be_present_in_element((By.ID,"delayedContent"),"数据加载完成"))
now = datetime.now()
assert now.strftime("%H:%M") in delayed_Content.text,"时间不符"
print(delayed_Content.text)

time.sleep(3)
driver.quit()