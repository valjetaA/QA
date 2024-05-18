from controllers.ChromeController import ChromeController
import unittest
import time

SITE_URL = 'http://shop.qatl.ru/'
FIRST_PRODUCT = 'QWER'
SECOND_PRODUCT = '1234'
ADD_TO_CART = 'ADD TO CART'
FIRST_PR_TABLE_COL_XPATH = '/html/body/div[7]/div/div/div[2]/div/table/tbody/tr[1]/td[2]/a'
SECOND_PR_TABLE_COL_XPATH = '/html/body/div[7]/div/div/div[2]/div/table/tbody/tr[2]/td[2]/a'
CLOSE_CLASS = 'close'


class AddProductToCart(unittest.TestCase):
    def setUp(self) -> None:        
        self._controller = ChromeController()
        self._controller.open_page(SITE_URL)
    
    def tearDown(self) -> None:
        self._controller.close()
    
    def test_add_one_product(self):
        self._controller.click_on_hyperlink(FIRST_PRODUCT)
        self._controller.click_on_hyperlink(ADD_TO_CART)
        time.sleep(2)
        elem = self._controller.find_elem_by_xpath(FIRST_PR_TABLE_COL_XPATH)
        self.assertTrue(elem.text, FIRST_PRODUCT.lower())
    
    def test_add_two_product(self):
        self._controller.click_on_hyperlink(FIRST_PRODUCT)
        self._controller.click_on_hyperlink(ADD_TO_CART)
        time.sleep(2)
        self._controller.click_on_button(CLOSE_CLASS)
        self._controller.go_back()
        self._controller.click_on_hyperlink(SECOND_PRODUCT)
        self._controller.click_on_hyperlink(ADD_TO_CART)
        time.sleep(2)
        elem1 = self._controller.find_elem_by_xpath(FIRST_PR_TABLE_COL_XPATH)
        elem2 = self._controller.find_elem_by_xpath(SECOND_PR_TABLE_COL_XPATH)
        self.assertTrue(elem1.text, FIRST_PRODUCT.lower())
        self.assertTrue(elem2.text, SECOND_PRODUCT.lower())
