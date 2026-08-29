from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TablePage(BasePage):
    """表格练习页面封装类"""

    def get_table_rows(self):
        """获取表格所有行"""
        table = self.driver.find_element(By.ID, "dataTable")
        return table.find_elements(By.TAG_NAME, "tr")

    def get_row_cells(self, row):
        """获取某一行的所有单元格"""
        return row.find_elements(By.TAG_NAME, "td")

    def find_city_by_name(self, name):
        """根据姓名查找所在城市，找不到返回 None"""
        rows = self.get_table_rows()
        for row in rows[1:]:  # 跳过表头
            cells = self.get_row_cells(row)
            if len(cells) > 0 and cells[0].text == name:
                return cells[2].text
        return None

    def get_name_column_values(self):
        """获取姓名列的所有值"""
        names = []
        rows = self.get_table_rows()
        for row in rows:
            cells = self.get_row_cells(row)
            if len(cells) > 0:
                names.append(cells[0].text)
        return names
