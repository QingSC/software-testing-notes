import allure
import pytest
from pages.table_page import TablePage


pytestmark = pytest.mark.table


@allure.feature("表格功能")
@allure.story("表格数据校验")
@allure.severity(allure.severity_level.NORMAL)
class TestTable:
    """表格测试类"""

    @allure.title("表格总行数")
    @allure.description("测试表格总行数是否为 4 行（1 行表头 + 3 行数据）")
    def test_table_row_count(self, driver):
        page = TablePage(driver)
        page.open()

        rows = page.get_table_rows()
        assert len(rows) == 4, f"期望 4 行，实际 {len(rows)} 行"

    @allure.title("根据姓名查找城市")
    @allure.description("测试李四所在行的城市是否为上海")
    def test_find_li_si_city(self, driver):
        page = TablePage(driver)
        page.open()

        city = page.find_city_by_name("李四")
        assert city is not None, "表格中未找到李四"
        assert city == "上海", f"李四所在城市不是上海，而是 {city}"

    @allure.title("姓名列数据校验")
    @allure.description("测试姓名列的数据是否都在预期范围内")
    def test_name_column_values(self, driver):
        page = TablePage(driver)
        page.open()

        names = page.get_name_column_values()
        for name in names:
            assert name in ["张三", "李四", "王五"], f"姓名 {name} 不在预期范围内"

    @allure.title("第二行单元格数据")
    @allure.description("测试表格第二行（索引 2，即第三行）的单元格数据")
    def test_second_row_cells(self, driver):
        page = TablePage(driver)
        page.open()

        rows = page.get_table_rows()
        cells = page.get_row_cells(rows[2])
        for cell in cells:
            assert cell.text in ["李四", "30", "上海"], f"单元格值 {cell.text} 不在预期范围内"
