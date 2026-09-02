import allure
import pytest
from pages.advanced_page import AdvancedPage

pytestmark = pytest.mark.advanced

@allure.feature("高级 Selenium 操作")
@allure.story("JavaScript 执行与高级等待")
@allure.severity(allure.severity_level.NORMAL)
class TestAdvanced:
    """高级 Selenium 操作测试类"""

    @allure.title("JS 移除只读属性并输入")
    @allure.description("测试用 JavaScript 移除 readonly 属性后，可以向只读输入框输入内容")
    def test_js_readonly_input(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.set_readonly_input_value("2026-08-31")
        assert page.get_readonly_value_text() == "2026-08-31", "只读输入框的值没有被成功修改"

    @allure.title("JS 滚动并加载更多")
    @allure.description("测试用 JavaScript 滚动到按钮后，点击加载更多")
    def test_js_scroll_and_load_more(self, driver):
        page = AdvancedPage(driver)
        page.open()

        before_count = page.get_scroll_items_count()
        page.scroll_to_load_more_button()
        page.click_load_more()
        after_count = page.get_scroll_items_count()

        assert after_count == before_count + 3, f"加载后项目数应为 {before_count + 3}，实际为 {after_count}"

    @allure.title("等待按钮可点击")
    @allure.description("测试显式等待按钮从不可见到可点击")
    def test_wait_for_clickable_button(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.click_appear_trigger_button()
        button = page.wait_for_clickable_button(timeout=10)
        button.click()

        assert page.get_clickable_button_text() == "✅ 已点击","按钮点击后文本不正确"

    @allure.title("等待元素可见")
    @allure.description("测试显式等待隐藏方块变为可见")
    def test_wait_for_visible_box(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.click_show_visible_button()
        page.wait_for_visible_box(timeout=10)

        assert page.get_visible_box_text() == "我现在可见了", "可见方块文本不正确"

    @allure.title("等待元素出现在 DOM 中")
    @allure.description("测试显式等待延迟创建的元素出现")
    def test_wait_for_new_element(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.click_add_element_button()
        page.wait_for_new_element(timeout=10)

        assert page.get_new_element_text() == "我是延迟添加的元素", "新元素文本不正确"

    @allure.title("等待文本出现")
    @allure.description("测试显式等待元素文本发生变化")
    def test_wait_for_dynamic_text(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.click_change_text_button()
        page.wait_for_dynamic_text("✅ 文本已改变", timeout=10)

        assert page.get_dynamic_text() == "✅ 文本已改变", "动态文本不正确"

    @allure.title("等待元素消失")
    @allure.description("测试显式等待元素从页面消失")
    def test_wait_for_disappear_box(self, driver):
        page = AdvancedPage(driver)
        page.open()

        page.click_disappear_trigger_button()
        page.wait_for_box_disappear(timeout=10)

        assert not page.is_box_visible(), "红色方块仍然可见"

