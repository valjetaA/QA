from controllers.ChromeController import ChromeController
import unittest
import json
from parameterized import parameterized

SITE_URL = 'http://shop.qatl.ru/'
AUTH_TEST_FILE_PATH = './test-data/auth.json'
ACCOUNT = 'Account'
ENTER = 'Вход'
LOGIN_STR = 'login'
PASSWORD_STR = 'password'
ALERT_SUCCESS = 'alert-success'
ALERT_DANGER = 'alert-danger'
BTN_CLASS = 'btn'
HAS_SUCCESS = 'has-success'
HAS_ERROR = 'has-error'

class TestAuthorization(unittest.TestCase):
    def setUp(self) -> None:
        with open(AUTH_TEST_FILE_PATH) as f:
            self._test_data = json.load(f)
        self._controller = ChromeController()
        self._controller.open_page(SITE_URL)
        self._controller.click_on_hyperlink(ACCOUNT)
        self._controller.click_on_hyperlink(ENTER)

    def tearDown(self) -> None:
        self._controller.close()

    @parameterized.expand([
        ['valid',  ALERT_SUCCESS],
        ['invalid', ALERT_DANGER]
    ])
    def test_auth(self, name, msg):
        item = self._test_data[name]
        self._controller.enter_value_in_input(LOGIN_STR, item[LOGIN_STR])
        self._controller.enter_value_in_input(PASSWORD_STR, item[PASSWORD_STR])
        self.assertTrue(self._controller.check_availaility(HAS_SUCCESS), msg='error with success icon')
        self._controller.click_on_button(BTN_CLASS)
        self.assertTrue(self._controller.check_availaility(msg), msg=f'error with {msg}')

    def test_auth_with_empty_data(self):
        item = self._test_data['empty']
        self._controller.enter_value_in_input(LOGIN_STR, item[LOGIN_STR])
        self._controller.enter_value_in_input(PASSWORD_STR, item[PASSWORD_STR])
        self.assertTrue(self._controller.check_availaility(HAS_ERROR), msg='error with error icon')
        self._controller.click_on_button(BTN_CLASS)
        self.assertFalse(self._controller.check_availaility(ALERT_SUCCESS), msg='error with alert')
        self.assertFalse(self._controller.check_availaility(ALERT_DANGER), msg='error with alert')
