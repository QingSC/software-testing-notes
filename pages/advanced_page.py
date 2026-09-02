from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdvancedPage(BasePage):
    """高级 Selenium 操作练习页面封装类"""

    def open(self):
        """打开高级练习页面"""
        file_path = self.driver.config.get("advanced_url")
        self.driver.logger.info(f"打开高级练习页面：{file_path}")
        self.driver.get(f"file:///{file_path}")

    # -------------------- JavaScript 执行相关 --------------------

    def set_readonly_input_value(self, value):
        """用 JavaScript 移除 readonly 属性后输入值"""
        self.driver.logger.info(f"JS 设置只读输入框值为：{value}")
        element = self.driver.find_element(By.ID, "readonlyInput")

        # 移除 readonly 属性，否则无法输入
        self.driver.execute_script("arguments[0].removeAttribute('readonly');", element)

        # 清空并输入新值
        element.clear()
        element.send_keys(value)

    def get_readonly_value_text(self):
        """获取页面上显示的只读输入框当前值"""
        text = self.driver.find_element(By.ID, "readonlyValue").text
        self.driver.logger.info(f"只读输入框显示值：{text}")
        return text

    def click_load_more(self):
        """点击加载更多按钮"""
        self.driver.logger.info("点击加载更多按钮")
        self.driver.find_element(By.ID, "loadMoreBtn").click()

    def scroll_to_load_more_button(self):
        """用 JavaScript 滚动到加载更多按钮"""
        self.driver.logger.info("滚动到加载更多按钮")
        button = self.driver.find_element(By.ID, "loadMoreBtn")
        self.driver.execute_script("arguments[0].scrollIntoView();", button)

    def get_scroll_items_count(self):
        """获取滚动区域中的项目数量"""
        items = self.driver.find_elements(By.CSS_SELECTOR, "#scrollContainer .item")
        self.driver.logger.info(f"滚动区域项目数量：{len(items)}")
        return len(items)

    # -------------------- 高级等待相关 --------------------

    def click_appear_trigger_button(self):
        """点击触发延迟显示可点击按钮"""
        self.driver.logger.info("点击触发可点击按钮显示")
        self.driver.find_element(By.ID, "appearBtn").click()

    def wait_for_clickable_button(self, timeout=10):
        """显式等待按钮可见且可点击"""
        self.driver.logger.info(f"等待可点击按钮，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        button = wait.until(EC.element_to_be_clickable((By.ID, "clickableBtn")))
        self.driver.logger.info("可点击按钮已出现")
        return button

    def click_clickable_button(self):
        """点击延迟出现的可点击按钮"""
        self.driver.logger.info("点击延迟出现的可点击按钮")
        self.driver.find_element(By.ID, "clickableBtn").click()

    def get_clickable_button_text(self):
        """获取可点击按钮的文本"""
        text = self.driver.find_element(By.ID, "clickableBtn").text
        self.driver.logger.info(f"可点击按钮文本：{text}")
        return text

    def click_show_visible_button(self):
        """点击触发橙色方块显示"""
        self.driver.logger.info("点击触发可见方块显示")
        self.driver.find_element(By.ID, "showVisibleBtn").click()

    def wait_for_visible_box(self, timeout=10):
        """显式等待橙色方块可见"""
        self.driver.logger.info(f"等待可见方块，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        box = wait.until(EC.visibility_of_element_located((By.ID, "visibleBox")))
        self.driver.logger.info("可见方块已显示")
        return box

    def get_visible_box_text(self):
        """获取橙色方块的文本"""
        text = self.driver.find_element(By.ID, "visibleBox").text
        self.driver.logger.info(f"可见方块文本：{text}")
        return text

    def click_add_element_button(self):
        """点击触发延迟添加新元素"""
        self.driver.logger.info("点击触发添加新元素")
        self.driver.find_element(By.ID, "addElementBtn").click()

    def wait_for_new_element(self, timeout=10):
        """显式等待新元素出现在 DOM 中"""
        self.driver.logger.info(f"等待新元素出现，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.ID, "newDynamicElement")))
        self.driver.logger.info("新元素已添加到 DOM")
        return element

    def get_new_element_text(self):
        """获取延迟添加的新元素文本"""
        text = self.driver.find_element(By.ID, "newDynamicElement").text
        self.driver.logger.info(f"新元素文本：{text}")
        return text

    def click_change_text_button(self):
        """点击触发文本变化"""
        self.driver.logger.info("点击触发文本变化")
        self.driver.find_element(By.ID, "changeTextBtn").click()

    def wait_for_dynamic_text(self, text, timeout=10):
        """显式等待指定文本出现在 dynamicText 元素中"""
        self.driver.logger.info(f"等待文本出现：{text}，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.text_to_be_present_in_element((By.ID, "dynamicText"), text))
        self.driver.logger.info(f"文本已出现：{text}")

    def get_dynamic_text(self):
        """获取 dynamicText 元素的当前文本"""
        text = self.driver.find_element(By.ID, "dynamicText").text
        self.driver.logger.info(f"动态文本内容：{text}")
        return text

    def click_disappear_trigger_button(self):
        """点击触发红色方块消失"""
        self.driver.logger.info("点击触发红色方块消失")
        self.driver.find_element(By.ID, "disappearTriggerBtn").click()

    def wait_for_box_disappear(self, timeout=10):
        """显式等待红色方块从页面消失"""
        self.driver.logger.info(f"等待红色方块消失，超时时间：{timeout} 秒")
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.invisibility_of_element_located((By.ID, "disappearBox")))
        self.driver.logger.info("红色方块已消失")

    def is_box_visible(self):
        """判断红色方块是否可见"""
        visible = self.driver.find_element(By.ID, "disappearBox").is_displayed()
        self.driver.logger.info(f"红色方块是否可见：{visible}")
        return visible
