from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class ChromeController:
    _SCRIPT_GO_BACK = "window.history.go(-1)"
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        self._driver = webdriver.Chrome(options=options)
    
    def open_page(self, url):
        self._driver.get(url)

    def enter_value_in_input(self, input_name, value):
        elem = self._driver.find_element(By.NAME, input_name)
        elem.send_keys(value)

    def click_on_button(self, button_class_name):
        elem = self._driver.find_element(By.CLASS_NAME, button_class_name)
        elem.click()
    
    def click_on_hyperlink(self, hyperlink_text):
        elem = self._driver.find_element(By.LINK_TEXT, hyperlink_text)
        elem.click()

    def enter_value_in_input_with_enter(self, input_name, value):
        elem = self._driver.find_element(By.NAME, input_name)
        elem.send_keys(value)
        elem.send_keys(Keys.RETURN)
    
    def find_elem_by_xpath(self, xpath):
        elem = self._driver.find_element(By.XPATH, xpath)
        return elem
    
    def go_back(self):
        self._driver.execute_script(self._SCRIPT_GO_BACK)
    
    def check_availaility(self, elem_class_name):
        try:
            elem = self._driver.find_element(By.CLASS_NAME, elem_class_name)
            return True
        except:
            return False
    
    def close(self):
        self._driver.close()
