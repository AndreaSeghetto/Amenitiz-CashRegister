from django.test import TestCase
from .models import Products
from django.urls import reverse

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