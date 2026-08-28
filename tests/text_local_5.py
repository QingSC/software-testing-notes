from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time


driver = webdriver.Edge()
# 用绝对路径访问本地文件
file_path = os.path.abspath("../pages/practice.html")
driver.get(f"file:///{file_path}")

##5.1获取表格中所有行的数据
# 获取整个表格
table = driver.find_element(By.ID,"dataTable")
# 获取所有行（<tr>）
rows = table.find_elements(By.TAG_NAME,"tr")

#判断总数是否为4行
assert len(rows)==4 ,"总行数不为4行"

# 遍历所有行
first_row = rows[0]
first_row_cells = first_row.find_elements(By.TAG_NAME,"th")
for cell in first_row_cells:
    print(cell.text,end=" ")
for row in rows:
    cells = row.find_elements(By.TAG_NAME,"td")
    for cell in cells:
        print(cell.text,end=" ")
    print()

##5.2获取“李四”所在行的“城市”信息
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME,"td")
    if len(cells) > 0 and cells[0].text == "李四":
        city = cells[2].text
        assert city == "上海",f"查询到李四所在城市不是上海，而是{city}"
        print(f"李四所在城市：{city}")


##5.3获取所有“姓名”列的数据
names = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME,"td")
    if len(cells) > 0:
        names.append(cells[0].text)
for name in names:
    assert name in ["张三","李四","王五"],f"不在“张三”“李四”“王五”中，元素是{name}"
    print(name,end=" ")
print()

##5.4获取第二行（索引1）的所有单元格数据
cells = rows[2].find_elements(By.TAG_NAME,"td")
for cell in cells:
    assert cell.text in ["李四","30","上海"],f"值不在其中，为{cell.text}"
    print(cell.text,end=" ")

time.sleep(3)
driver.quit()