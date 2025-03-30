import json
from django.test import TestCase, Client
from .models import Products
from django.urls import reverse
from .utils import calculate_total

class ProductsModelTest(TestCase):
    def test_create_product(self):
        # Create a product instance
        product = Products.objects.create(
            product_code="GR1",
            name="Green Tea",
            price=3.11
        )
        # Verify that the product is saved in the database
        self.assertEqual(Products.objects.count(), 1)
        # Check that the product fields are set correctly
        self.assertEqual(product.product_code, "GR1")
        self.assertEqual(product.name, "Green Tea")
        self.assertEqual(product.price, 3.11)

class ProductsAPITest(TestCase):
    def setUp(self):
        # Create some sample products in the test database
        Products.objects.create(product_code="CF1", name="Coffee", price=11.23)
        Products.objects.create(product_code="SR1", name="Strawberries", price=5.00)

    def test_products_api_returns_json(self):
        # Call the API endpoint
        response = self.client.get(reverse('products_api'))

        # Check that the response is successful (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Check that the response is in JSON format
        self.assertEqual(response['Content-Type'], 'application/json')

        # Parse the JSON and check contents
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Coffee")
        self.assertEqual(data[1]['name'], "Strawberries")
        
class CalculateTotalTest(TestCase):
    def setUp(self):
        # Populate the test database with the three products
        Products.objects.create(product_code="GR1", name="Green Tea", price=3.11)
        Products.objects.create(product_code="SR1", name="Strawberries", price=5.00)
        Products.objects.create(product_code="CF1", name="Coffee", price=11.23)

    def test_checkout_scenario_1(self):
        codes = ["GR1", "GR1"]
        total = calculate_total(codes)
        # buy-one-get-one-free
        self.assertEqual(total, 3.11)  

    def test_checkout_scenario_2(self):
        codes = ["SR1", "SR1", "GR1", "SR1"]
        total = calculate_total(codes)
        # 3 strawberries discounted + 1 tea
        self.assertEqual(total, 16.61)  

    def test_checkout_scenario_3(self):
        codes = ["GR1", "CF1", "SR1", "CF1", "CF1"]
        total = calculate_total(codes)
        # 3 coffees with discount, 1 strawberry, 1 tea
        self.assertEqual(total, 30.57) 

class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create sample products for testing
        Products.objects.create(product_code="GR1", name="Green Tea", price=3.11)
        Products.objects.create(product_code="CF1", name="Coffee", price=5.00)

    def test_checkout_valid_items(self):
        # Send a POST request with valid product codes
        response = self.client.post(
            reverse('checkout_view'),
            data=json.dumps({"items": ["GR1", "CF1", "GR1"]}),
            content_type='application/json'
        )
        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)
        # Check total and summary        
        self.assertEqual(response.json()['total'], 8.11)
        self.assertEqual(len(response.json()['summary']), 2)  
        # Validate quantity per product in summary
        summary = response.json()['summary']
        self.assertTrue(any(item['product_code'] == 'GR1' and item['quantity'] == 2 for item in summary))
        self.assertTrue(any(item['product_code'] == 'CF1' and item['quantity'] == 1 for item in summary))      

    def test_checkout_invalid_item(self):
        # Send a POST request with only an invalid product code
        response = self.client.post(
            reverse('checkout_view'),
            data=json.dumps({"items": ["INVALID_CODE"]}),
            content_type='application/json'
        )
        # The total should be 0 and summary should be empty
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total'], 0)
        self.assertEqual(len(response.json()['summary']), 0)

    def test_checkout_mixed_valid_and_invalid_items(self):
        # Add another product to test a mixed case
        Products.objects.create(product_code="SR1", name="Strawberries", price=5.00)
        # Send a POST request with both valid and invalid codes
        response = self.client.post(
            reverse('checkout_view'),
            data=json.dumps({"items": ["SR1", "INVALID_CODE", "SR1"]}),
            content_type='application/json'
        )
        # The invalid item should be ignored
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total'], 10.00)
        self.assertEqual(len(response.json()['summary']), 1)
        self.assertEqual(response.json()['summary'][0]['product_code'], 'SR1')
        self.assertEqual(response.json()['summary'][0]['quantity'], 2)    