import allure
import pytest
from pages.textarea_page import TextareaPage


pytestmark = pytest.mark.textarea


@allure.feature("文本框与动态内容功能")
@allure.story("文本域输入与动态内容更新")
@allure.severity(allure.severity_level.NORMAL)
class TestTextareaDynamic:
    """文本框与动态内容测试类"""

    @allure.title("文本域输入")
    @allure.description("测试在文本域中输入内容")
    def test_textarea_input(self, driver):
        page = TextareaPage(driver)
        page.open()

        page.input_comment("自动化测试练习")
        value = page.get_comment_value()

        assert value == "自动化测试练习", f"文本域内容不符：{value}"

    @allure.title("动态内容更新")
    @allure.description("测试点击更新按钮后动态内容显示")
    def test_update_dynamic_content(self, driver):
        page = TextareaPage(driver)
        page.open()

        page.input_comment("自动化测试练习")
        page.click_update_button()

        text = page.get_dynamic_content_text()
        assert "自动化测试练习" in text, f"动态内容不符：{text}"

    @allure.title("显示隐藏区域")
    @allure.description("测试点击按钮后显示隐藏区域")
    def test_show_hidden_content(self, driver):
        page = TextareaPage(driver)
        page.open()

        page.click_show_hidden_button()
        assert page.is_hidden_content_displayed(), "隐藏区域未显示"

    @allure.title("重新隐藏区域")
    @allure.description("测试再次点击后隐藏区域重新隐藏")
    def test_hide_content_again(self, driver):
        page = TextareaPage(driver)
        page.open()

        page.click_show_hidden_button()
        page.click_show_hidden_button()
        assert not page.is_hidden_content_displayed(), "隐藏区域仍然显示"
