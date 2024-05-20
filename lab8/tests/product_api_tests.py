from os import path
import os
from product_api import ProductsApi
import json
import jsonschema
import unittest
from parameterized import parameterized

class TestProductsApi(unittest.TestCase):
    _CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'conf'))

    _PRODUCTS_FILE = 'test-product-values.json'
    _PRODUCTS_SCHEMA_FILE = 'schema.json'
    def setUp(self):
        self._api = ProductsApi()
        self._created_product_ids = []
        self._products = self._load_config_json(self._PRODUCTS_FILE)
        self._schema = self._load_config_json(self._PRODUCTS_SCHEMA_FILE)

    def tearDown(self):
        for product_id in self._created_product_ids:
            self._api.delete(product_id)

    def _load_config_json(self, file_path):
        full_path = path.join(self._CONFIG_DIR, file_path)
        with open(full_path, encoding='utf-8') as f:
            return json.load(f)

    def _json_matches_schema(self, data):
        try:
            jsonschema.validate(data, self._schema)
            return True
        except:
            return False
    


    # Проверяет успешное добавление продукта с корректными значениями (сверка с массивом продуктов).
    def test_AddingProduct_WithCorrectValues_Succeeds_WithCheckList(self):        
        response = self._api.add(self._products['correctProduct'])
        self._created_product_ids.append(response['id']) 

        products = self._api.list()
        list_product = self._find_product(products, response['id'])

        self.assertEqual(response['status'], 1, 'Failed to add product')
        self.assertTrue(self._products['correctProduct'].items() <= list_product.items(), 'Failed to add product to list')
    
    # Проверяет успешное удаление продукта (сверка с массивом продуктов).
    def test_DeletingProductFromTheList(self):
        create_product = self._api.add(self._products['correctProduct'])
        response = self._api.delete(create_product['id'])

        products = self._api.list()
        list_product = self._find_product(products, create_product['id'])

        self.assertEqual(response['status'], 1, 'Response should be 1')
        self.assertIsNone(list_product, 'Product should be deleted')

    def _find_product(self, products, id):
        for product in products:
            if int(product['id']) == id:
                return product
        return None
    
    # Проверяет алиасы при добавлении двух одинаковых продуктов
    def test_CreatingWithTheSameAlias_AddsPostfix(self):
        response1 = self._api.add(self._products['checkProductsWithSameAlias'])
        self._created_product_ids.append(response1['id']) 
        response2 = self._api.add(self._products['checkProductsWithSameAlias'])
        self._created_product_ids.append(response2['id']) 

        products = self._api.list()
        list_product1 = self._find_product(products, response1['id'])
        list_product2 = self._find_product(products, response2['id'])

        self.assertEqual(list_product1['alias'], self._products['checkProductsWithSameAlias']['alias'], 'First alias should not have -0 postfix')
        self.assertEqual(list_product2['alias'], self._products['checkProductsWithSameAlias']['alias'] + '-0', 'Second alias should have -0 postfix')

    # Проверяет успешное добавление отредактированного продукта с корректными значениями.
    def test_AddingProduct_WithCorrectValues_Edited_Succeeds(self):
        response = self._api.add(self._products['correctProductEdited'])
        self._created_product_ids.append(response['id']) 
        self.assertEqual(response['status'], 1, 'Failed to add edited product')

    @parameterized.expand([
        ("correctProductEdited", 1),
        ("productWithStringPrice", 0),
        ("productWithNegativePrice", 0),
        ("productWithNullCategory", 0),
        ("productWithInvalid0Category", 1),
        ("productWithValid15Category", 1),
        ("productWithInvalid16Category", 1),
        ("productWithInvalidId", 1),
        ("productWithNullStatus", 1),
        ("productWithInvalidStatus", 1),
        ("productWithNullHit", 1),
        ("productWithInvalidHit", 1),
        ("productWithMissingProps", 0),
        ("emptyProduct", 0),
        ("nullProduct", 0)
    ])
    
    def test_AddingProduct_WithVariousValues_ReturnsExpectedStatus(self, product_key, expected_status):
        response = self._api.add(self._products[product_key])
        if expected_status == 1:
            self._created_product_ids.append(response['id'])
        self.assertEqual(response['status'], expected_status, f"Failed to add product: {product_key}")


if __name__ == '__main__':
    unittest.main()