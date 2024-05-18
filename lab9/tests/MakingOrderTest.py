from controllers.ChromeController import ChromeController
import unittest
from parameterized import parameterized
import time
import json

SITE_URL = 'http://shop.qatl.ru/'
AUTH_TEST_FILE_PATH = './test-data/auth.json'
ACCOUNT = 'Account'
ENTER = 'Вход'
LOGIN_STR = 'login'
PASSWORD_STR = 'password'
FIRST_PRODUCT = 'QWER'
ADD_TO_CART = 'ADD TO CART'
FIRST_PR_TABLE_COL_XPATH = "//a[text()='qwer']"
BTN_DEFAULT_CLASS = 'btn-default'
ERROR_MSG_XPATH = '//body/h1'
ERROR_MSG = 'Произошла ошибка'
MAKING_ORDER_TEST_PATH = './test-data/making_order.json'
BTN_XPATH = "//button[@type='submit']"
BTN_PRIMARY_CLASS = 'btn-primary'
NAME_STR = 'name'
EMAIL_STR = 'email'
ADDRESS_STR = 'address'
BTN_CLASS = 'btn'
LOGO_XPATH = '//h1'
ALERT_DANGER = 'alert-danger'


class MakingOrderTest(unittest.TestCase):
    def setUp(self) -> None:        
        self._controller = ChromeController()
        self._controller.open_page(SITE_URL)
    def tearDown(self) -> None:
        self._controller.close()

    def test_with_auth(self):
        self._controller.click_on_hyperlink(ACCOUNT)
        self._controller.click_on_hyperlink(ENTER)
        test_data = self.load_test_data_from_file(AUTH_TEST_FILE_PATH, 'valid')
        self._controller.enter_value_in_input(LOGIN_STR, test_data[LOGIN_STR])
        self._controller.enter_value_in_input(PASSWORD_STR, test_data[PASSWORD_STR])
        self._controller.click_on_button(BTN_CLASS)
        self._controller.find_elem_by_xpath(LOGO_XPATH).click()
        self.add_to_cart()
        elem = self._controller.find_elem_by_xpath(FIRST_PR_TABLE_COL_XPATH)
        self.assertEqual(elem.text, FIRST_PRODUCT.lower(), msg='error with name product')    
        self._controller.click_on_button(BTN_DEFAULT_CLASS)
        err_msg = self._controller.find_elem_by_xpath(ERROR_MSG_XPATH).text
        self.assertEqual(err_msg, ERROR_MSG, msg='Error with redirect to error page')    

    def test_without_auth(self):        
        self.add_to_cart()
        elem = self._controller.find_elem_by_xpath(FIRST_PR_TABLE_COL_XPATH)
        self.assertEqual(elem.text, FIRST_PRODUCT.lower(), msg='error with name product')
        test_data = self.load_test_data_from_file(MAKING_ORDER_TEST_PATH, 'valid')
        self.fill_inputs_for_make_order(test_data)
        self._controller.find_elem_by_xpath(BTN_XPATH).click()
        err_msg = self._controller.find_elem_by_xpath(ERROR_MSG_XPATH).text
        self.assertEqual(err_msg, ERROR_MSG, msg='Error with redirect to error page')

    @parameterized.expand([
        ['with_busy_email'],
        ['with_busy_login']
    ])

    def test_without_auth_with_busy_parameters(self, name):
        self.add_to_cart()
        test_data = self.load_test_data_from_file(MAKING_ORDER_TEST_PATH, name)
        self.fill_inputs_for_make_order(test_data)
        self._controller.find_elem_by_xpath(BTN_XPATH).click()
        time.sleep(1)
        self.assertTrue(self._controller.check_availaility(ALERT_DANGER), msg=f'error with alert msg for {name}')

    def add_to_cart(self):
        self._controller.click_on_hyperlink(FIRST_PRODUCT)
        self._controller.click_on_hyperlink(ADD_TO_CART)
        time.sleep(2)
        self._controller.click_on_button(BTN_PRIMARY_CLASS)

    def fill_inputs_for_make_order(self, json_data):
        self._controller.enter_value_in_input(LOGIN_STR, json_data[LOGIN_STR])
        self._controller.enter_value_in_input(PASSWORD_STR, json_data[PASSWORD_STR])
        self._controller.enter_value_in_input(NAME_STR, json_data[NAME_STR])
        self._controller.enter_value_in_input(EMAIL_STR, json_data[EMAIL_STR])
        self._controller.enter_value_in_input(ADDRESS_STR, json_data[ADDRESS_STR])
        time.sleep(2)
        
    def load_test_data_from_file(self, file_path, json_name):
        test_data = None
        with open(file_path) as f:
            test_data = json.load(f)
            test_data = test_data[json_name]
        return test_data