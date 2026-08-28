from selenium.webdriver.common.by import By
import pytest
pytestmark = pytest.mark.table

def test_table_row_count(practice_page):
    """测试表格总行数是否为 4 行（1 行表头 + 3 行数据）"""
    table = practice_page.find_element(By.ID, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    assert len(rows) == 4, f"期望 4 行，实际 {len(rows)} 行"


def test_find_li_si_city(practice_page):
    """测试李四所在行的城市是否为上海"""
    table = practice_page.find_element(By.ID, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # 跳过表头，从第 2 行开始遍历
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0 and cells[0].text == "李四":
            city = cells[2].text
            assert city == "上海", f"李四所在城市不是上海，而是 {city}"
            return

    # 如果遍历完都没找到李四，断言失败
    assert False, "表格中未找到李四"


def test_name_column_values(practice_page):
    """测试姓名列的数据是否都在预期范围内"""
    table = practice_page.find_element(By.ID, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    names = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0:
            names.append(cells[0].text)

    for name in names:
        assert name in ["张三", "李四", "王五"], f"姓名 {name} 不在预期范围内"


def test_second_row_cells(practice_page):
    """测试表格第二行（索引 2，即第三行）的单元格数据"""
    table = practice_page.find_element(By.ID, "dataTable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    cells = rows[2].find_elements(By.TAG_NAME, "td")
    for cell in cells:
        assert cell.text in ["李四", "30", "上海"], f"单元格值 {cell.text} 不在预期范围内"
