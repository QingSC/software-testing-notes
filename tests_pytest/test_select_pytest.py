import allure
import pytest
from pages.select_page import SelectPage


pytestmark = pytest.mark.select


@allure.feature("下拉框功能")
@allure.story("城市与爱好选择")
@allure.severity(allure.severity_level.NORMAL)
class TestSelect:
    """下拉框测试类"""

    @allure.title("城市下拉框切换")
    @allure.description("测试城市从深圳切换为广州")
    def test_select_city_change(self, driver):
        page = SelectPage(driver)
        page.open()

        # 先选择深圳
        page.select_city_by_value("shenzhen")
        assert page.get_city_selected_text() == "深圳", f"期望选中'深圳'，实际选中：{page.get_city_selected_text()}"

        # 再重新选择广州
        page.select_city_by_value("guangzhou")
        assert page.get_city_selected_text() == "广州", f"期望选中'广州'，实际选中：{page.get_city_selected_text()}"

    @allure.title("爱好多选")
    @allure.description("测试同时选中编程和运动")
    def test_select_hobby_multiple(self, driver):
        page = SelectPage(driver)
        page.open()

        # 选中编程和运动
        page.select_hobby_by_value("coding")
        page.select_hobby_by_value("sports")

        # 获取所有选中的选项
        all_selected = page.get_hobby_selected_texts()
        # 断言每个选中的选项都在预期列表中
        for option in all_selected:
            assert option in ["编程", "运动"], f"未预期的选中项：{option}"

    @allure.title("取消爱好选择")
    @allure.description("测试取消勾选编程后只剩运动")
    def test_deselect_hobby_coding(self, driver):
        page = SelectPage(driver)
        page.open()

        # 先选中编程和运动
        page.select_hobby_by_value("coding")
        page.select_hobby_by_value("sports")

        # 取消勾选编程
        page.deselect_hobby_by_value("coding")

        # 获取剩下的选中项
        all_selected = page.get_hobby_selected_texts()
        # 断言只剩一个选项，且是"运动"
        assert len(all_selected) == 1, f"期望只剩 1 个选中项，实际有 {len(all_selected)} 个"
        assert all_selected[0] == "运动", f"期望选中'运动'，实际选中：{all_selected[0]}"
