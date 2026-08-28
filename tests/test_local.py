from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

driver = webdriver.Edge()

# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

# 测试数据（用户名, 密码, 预期结果）
test_data = [
    ("admin","123456","登录成功"),
    ("","123456","请输入用户名"),
    ("admin","","请输入密码"),
    ("wronguser", "123456", "用户名或密码错误"),
     ("admin", "wrongpwd", "用户名或密码错误"),
]

for user, pwd, expected in test_data:
    # 定位元素
    username_input = driver.find_element(By.ID,"username")
    password_input = driver.find_element(By.ID,"password")
    login_btn = driver.find_element(By.ID,"loginBtn")

    # 清空并输入（关键步骤）
    username_input.clear()
    username_input.send_keys(user)
    password_input.clear()
    password_input.send_keys(pwd)

    login_btn.click()

    # 获取结果
    result = driver.find_element(By.ID,"loginResult").text
    print(f"输入: user ='{user}',pwd = '{pwd}' → 结果: '{result}'")

    # 断言
    assert expected in result,f"测试失败！预期包含 '{expected}'，实际为 '{result}'"

    time.sleep(0.5)

print("\n✅ 所有登录测试用例通过！")
driver.quit()





print("本地登录成功！")
time.sleep(3)
driver.quit()