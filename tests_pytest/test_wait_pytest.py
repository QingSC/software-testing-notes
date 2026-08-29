import pytest
from pages.wait_page import WaitPage


pytestmark = pytest.mark.wait


def test_load_delayed_content(driver):
    """测试点击加载按钮后，延迟内容最终显示完成"""
    page = WaitPage(driver)
    page.open()

    page.click_load_button()
    assert page.get_delayed_content_text() == "⏳ 加载中...", "未显示加载中"

    page.wait_for_content("数据加载完成")
    final_text = page.get_delayed_content_text()

    now_str = page.get_current_time_str("%H:%M")
    assert now_str in final_text, f"时间 {now_str} 未出现在文本中，实际文本：{final_text}"
