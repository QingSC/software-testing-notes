from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.maximize_window()

driver.get("https://www.baidu.com")

# 加大等待时间到15秒
wait = WebDriverWait(driver, 15)

try:
    # 方法1：用 ID 定位并等待可点击
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "kw")))
    search_box.send_keys("软件测试" + Keys.RETURN)
    print("✅ 搜索成功！")
except Exception as e:
    print(f"方法1失败: {e}")
    
    try:
        # 方法2：用 name 定位
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "wd")))
        search_box.send_keys("软件测试" + Keys.RETURN)
        print("✅ 搜索成功（用 name）！")
    except Exception as e2:
        print(f"方法2失败: {e2}")
        
        try:
            # 方法3：用 JavaScript 直接操作
            search_box = driver.find_element(By.ID, "kw")
            driver.execute_script("arguments[0].value = '软件测试';", search_box)
            driver.execute_script("document.getElementById('su').click();")
            print("✅ 搜索成功（用 JavaScript）！")
        except Exception as e3:
            print(f"所有方法都失败: {e3}")

time.sleep(3)
driver.quit()