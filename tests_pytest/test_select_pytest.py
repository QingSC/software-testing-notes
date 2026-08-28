from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest


pytestmark = pytest.mark.select


def test_select_city_change(practice_page):
    """测试城市下拉框从深圳改成广州"""
    city_select = Select(practice_page.find_element(By.ID, "citySelect"))

    # 先选择深圳
    city_select.select_by_value("shenzhen")
    selected = city_select.first_selected_option.text
    assert selected == "深圳", f"期望选中'深圳'，实际选中：{selected}"

    # 再重新选择广州
    city_select.select_by_value("guangzhou")
    selected = city_select.first_selected_option.text
    assert selected == "广州", f"期望选中'广州'，实际选中：{selected}"


def test_select_hobby_multiple(practice_page):
    """测试爱好下拉框多选：编程和运动"""
    hobby_select = Select(practice_page.find_element(By.ID, "hobbySelect"))

    # 选中编程和运动
    hobby_select.select_by_value("coding")
    hobby_select.select_by_value("sports")

    # 获取所有选中的选项
    all_selected = hobby_select.all_selected_options

    # 断言每个选中的选项都在预期列表中
    for option in all_selected:
        assert option.text in ["编程", "运动"], f"未预期的选中项：{option.text}"


def test_deselect_hobby_coding(practice_page):
    """测试取消勾选编程，只剩运动"""
    hobby_select = Select(practice_page.find_element(By.ID, "hobbySelect"))

    # 先选中编程和运动
    hobby_select.select_by_value("coding")
    hobby_select.select_by_value("sports")

    # 取消勾选编程
    hobby_select.deselect_by_value("coding")

    # 获取剩下的选中项
    all_selected = hobby_select.all_selected_options

    # 断言只剩一个选项，且是"运动"
    assert len(all_selected) == 1, f"期望只剩 1 个选中项，实际有 {len(all_selected)} 个"
    assert all_selected[0].text == "运动", f"期望选中'运动'，实际选中：{all_selected[0].text}"
