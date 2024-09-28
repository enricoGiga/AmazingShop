from django.contrib.auth.models import User
from django.test import TestCase

from .models import Product, Supplier


class ProductModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='supplier_user',
                                             password='password')

        self.supplier = Supplier.objects.create(user=self.user, name='Test Supplier')

    def test_create_product(self):
        product = Product.objects.create(
            supplier=self.supplier,
            name='Test Product',
            product_code='TP001',
            price=99.99,
            stock_status=Product.IN_STOCK
        )

        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.product_code, 'TP001')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.stock_status, Product.IN_STOCK)

    def test_product_string_representation(self):
        # Create a product
        product = Product.objects.create(
            supplier=self.supplier,
            name='Test Product',
            product_code='TP002',
            price=199.99,
            stock_status=Product.OUT_OF_STOCK
        )

        # Check the string representation
        self.assertEqual(str(product), 'Test Product (TP002)')

    def test_unique_together_constraint(self):
        Product.objects.create(
            supplier=self.supplier,
            name='Test Product',
            product_code='TP001',
            price=99.99,
            stock_status=Product.IN_STOCK
        )

        with self.assertRaises(Exception) as context:
            Product.objects.create(
                supplier=self.supplier,
                name='Another Product',
                product_code='TP001',  # Same product_code for the same supplier
                price=49.99,
                stock_status=Product.IN_STOCK
            )

        self.assertTrue('duplicate key value violates unique constraint' in str(context.exception))
