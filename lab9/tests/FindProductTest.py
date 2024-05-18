from controllers.ChromeController import ChromeController
import unittest
from parameterized import parameterized

SITE_URL = 'http://shop.qatl.ru/'
MEN_CATEGORY = 'Men'
WOMEN_CATEGORY = 'Women'
KIDS_CATEGORY = 'Kids'
CATEGORY_NAME_XPATH = '//ol/li[2]/a'
PRODUCT_CLASS = 'product-main'
FIND_INPUT_VAL = 'часы2'
FIND_INPUT_NAME = 's'

class FindProductTest(unittest.TestCase):
    def setUp(self) -> None:        
        self._controller = ChromeController()
        self._controller.open_page(SITE_URL)
    
    def tearDown(self) -> None:
        self._controller.close()
    
    @parameterized.expand([
        [MEN_CATEGORY],
        [WOMEN_CATEGORY],
        [KIDS_CATEGORY]
    ])

    def test_find_by_categories(self, category):
        self._controller.click_on_hyperlink(category)
        self.assertTrue(self._controller.check_availaility(PRODUCT_CLASS), msg=f'error with categor {category}')
        elem = self._controller.find_elem_by_xpath(CATEGORY_NAME_XPATH)
        self.assertEqual(elem.text, category, msg=f'error with name category - {category}')
    
    def test_find_by_input_with_non_empty_value(self):
        self._controller.enter_value_in_input_with_enter(FIND_INPUT_NAME, FIND_INPUT_VAL)
        self.assertTrue(self._controller.check_availaility(PRODUCT_CLASS), msg=f'error with find by input with non empty value')
    
    def test_find_by_input_with_empty_value(self):
        self._controller.enter_value_in_input_with_enter(FIND_INPUT_NAME, '')
        self.assertFalse(self._controller.check_availaility(PRODUCT_CLASS), msg=f'error with find by input with empty value')
