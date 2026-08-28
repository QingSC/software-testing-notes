from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytest
pytestmark = pytest.mark.wait

def test_load_delayed_content(practice_page):
    """测试点击加载按钮后，延迟内容最终显示完成"""
    # 点击加载按钮
    load_btn = practice_page.find_element(By.ID, "loadBtn")
    load_btn.click()

    # 立即检查是否显示"加载中"
    delayed_content = practice_page.find_element(By.ID, "delayedContent")
    assert delayed_content.text == "⏳ 加载中...", f"未显示加载中，实际：{delayed_content.text}"

    # 显式等待：最多 10 秒，直到内容包含"数据加载完成"
    wait = WebDriverWait(practice_page, 10)
    wait.until(EC.text_to_be_present_in_element((By.ID, "delayedContent"), "数据加载完成"))

    # 重新获取元素文本（等待后内容已更新）
    final_text = practice_page.find_element(By.ID, "delayedContent").text

    # 断言当前时间（时:分）出现在最终文本中
    now_str = datetime.now().strftime("%H:%M")
    assert now_str in final_text, f"时间 {now_str} 未出现在文本中，实际文本：{final_text}"
