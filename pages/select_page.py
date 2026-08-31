from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class SelectPage(BasePage):
    """下拉框练习页面封装类"""

    def select_city_by_value(self, value):
        """按 value 选择城市"""
        self.driver.logger.info(f"选择城市：{value}")
        city_select = Select(self.driver.find_element(By.ID, "citySelect"))
        city_select.select_by_value(value)

    def get_city_selected_text(self):
        """获取城市当前选中的文本"""
        city_select = Select(self.driver.find_element(By.ID, "citySelect"))
        text = city_select.first_selected_option.text
        self.driver.logger.info(f"当前选中城市：{text}")
        return text

    def select_hobby_by_value(self, value):
        """按 value 选择爱好"""
        self.driver.logger.info(f"选择爱好：{value}")
        hobby_select = Select(self.driver.find_element(By.ID, "hobbySelect"))
        hobby_select.select_by_value(value)

    def get_hobby_selected_texts(self):
        """获取所有选中的爱好文本，返回列表"""
        hobby_select = Select(self.driver.find_element(By.ID, "hobbySelect"))
        texts = [option.text for option in hobby_select.all_selected_options]
        self.driver.logger.info(f"当前选中爱好：{texts}")
        return texts

    def deselect_hobby_by_value(self, value):
        """按 value 取消选择爱好"""
        self.driver.logger.info(f"取消选择爱好：{value}")
        hobby_select = Select(self.driver.find_element(By.ID, "hobbySelect"))
        hobby_select.deselect_by_value(value)
