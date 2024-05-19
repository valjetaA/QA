from os import path
import os
from product_api import ProductsApi
import json
import jsonschema
import unittest

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

    # Проверяет успешное добавление продукта с корректными значениями.
    def test_AddingProduct_WithCorrectValues_Succeeds(self):
        response = self._api.add(self._products['correctProduct'])
        products = self._api.list()
        print(products)
        self.assertEqual(response['status'], 1, 'Failed to add product')

    # Проверяет успешное добавление отредактированного продукта с корректными значениями.
    def test_AddingProduct_WithCorrectValues_Edited_Succeeds(self):
        response = self._api.add(self._products['correctProductEdited'])
        self.assertEqual(response['status'], 1, 'Failed to add edited product')

    # Проверяет возвращение ошибки при попытке добавления продукта с ценой в виде строки.
    def test_AddingProduct_WithPriceAsString_ReturnsError(self):
        response = self._api.add(self._products['productWithStringPrice'])
        self.assertEqual(response['status'], 0, 'Failed to add product with string price')

    # Проверяет возвращение ошибки при попытке добавления продукта с отрицательной ценой.
    def test_AddingProduct_WithNegativePrice_ReturnsError(self):
        response = self._api.add(self._products['productWithNegativePrice'])
        self.assertEqual(response['status'], 0, 'Failed to add product with negative price')

    # Проверяет возвращение ошибки при попытке добавления продукта с нулевой категорией.
    def test_AddingProduct_WithNullCategory_ReturnsError(self):
        response = self._api.add(self._products['productWithNullCategory'])
        self.assertEqual(response['status'], 0, 'Failed to add product with null category')

    # Проверяет возвращение ошибки при попытке добавления продукта с недопустимой категорией (0).
    def test_AddingProduct_WithInvalidZeroCategory_ReturnsError(self):
        response = self._api.add(self._products['productWithInvalid0Category'])
        self.assertEqual(response['status'], 1, 'Failed to add product with invalid 0 category')
    
     # Проверяет успешное добавление продукта с категорией 15.
    def test_AddingProduct_WithValid15Category_Succeeds(self):
        response = self._api.add(self._products['productWithValid15Category'])
        self.assertEqual(response['status'], 1, 'Failed to add product with valid 15 category')

    # Проверяет возвращение ошибки при попытке добавления продукта с категорией 16.
    def test_AddingProduct_WithInvalid16Category_ReturnsError(self):
        response = self._api.add(self._products['productWithInvalid16Category'])
        self.assertEqual(response['status'], 1, 'Failed to add product with invalid 16 category')

    # Проверяет возвращение ошибки при попытке добавления продукта с недопустимым ID.
    def test_AddingProduct_WithInvalidId_ReturnsError(self):
        response = self._api.add(self._products['productWithInvalidId'])
        self.assertEqual(response['status'], 1, 'Failed to add product with invalid ID')

    # Проверяет возвращение ошибки при попытке добавления продукта с пустым статусом.
    def test_AddingProduct_WithNullStatus_ReturnsError(self):
        response = self._api.add(self._products['productWithNullStatus'])
        self.assertEqual(response['status'], 1, 'Failed to add product with null status')

    # Проверяет возвращение ошибки при попытке добавления продукта с недопустимым статусом.
    def test_AddingProduct_WithInvalidStatus_ReturnsError(self):
        response = self._api.add(self._products['productWithInvalidStatus'])
        self.assertEqual(response['status'], 1, 'Failed to add product with invalid status')

    # Проверяет возвращение ошибки при попытке добавления продукта с пустым hit.
    def test_AddingProduct_WithNullHit_ReturnsError(self):
        response = self._api.add(self._products['productWithNullHit'])
        self.assertEqual(response['status'], 1, 'Failed to add product with null hit')

    # Проверяет возвращение ошибки при попытке добавления продукта с недопустимым hit.
    def test_AddingProduct_WithInvalidHit_ReturnsError(self):
        response = self._api.add(self._products['productWithInvalidHit'])
        self.assertEqual(response['status'], 1, 'Failed to add product with invalid hit')

    # Проверяет возвращение ошибки при попытке добавления продукта с отсутствующими свойствами.
    def test_AddingProduct_WithMissingProps_ReturnsError(self):
        response = self._api.add(self._products['productWithMissingProps'])
        self.assertEqual(response['status'], 0, 'Failed to add product with missing properties')

    # Проверяет возвращение ошибки при попытке добавления пустого продукта.
    def test_AddingEmptyProduct_ReturnsError(self):
        response = self._api.add(self._products['emptyProduct'])
        self.assertEqual(response['status'], 0, 'Failed to add empty product')

    # Проверяет возвращение ошибки при попытке добавления нулевого продукта.
    def test_AddingNullProduct_ReturnsError(self):
        response = self._api.add(self._products['nullProduct'])
        self.assertEqual(response['status'], 0, 'Failed to add null product')
    
if __name__ == '__main__':
    unittest.main()