from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products_store.models import Supplier, Product


class BuyerDashboardViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.supplier = Supplier.objects.create(user=self.user)
        self.buyer_user = User.objects.create_user(username='buyer_user',
                                                   password='password')
        self.buyer_user.groups.add(1)  # user id 1 is the Buyer
        self.non_buyer_user = User.objects.create_user(username='non_buyer_user',
                                                       password='password')

        Product.objects.create(name='Test Product 1', product_code='TP001', price=100.00,
                               stock_status='In stock', supplier=self.supplier)
        Product.objects.create(name='Test Product 2', product_code='TP002', price=150.00,
                               stock_status='Out of stock', supplier=self.supplier)

    def test_buyer_dashboard_access(self):
        # Log in the buyer user
        self.client.login(username='buyer_user', password='password')

        # Access the buyer dashboard
        response = self.client.get(reverse('buyer_dashboard'))

        # Check if the response is successful and contains products in stock
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        self.assertNotContains(response,
                               'Test Product 2')  # Should not contain out of stock product

    def test_non_buyer_redirect(self):
        # Log in the non-buyer user
        self.client.login(username='non_buyer_user', password='password')

        # Attempt to access the buyer dashboard
        response = self.client.get(reverse('buyer_dashboard'))

        # Check if the response redirects to home
        self.assertRedirects(response, reverse('home'))


class SupplierDashboardViewTest(TestCase):

    def setUp(self):
        # Create a user and assign them to the Supplier group
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a Supplier object associated with the user
        self.supplier = Supplier.objects.create(user=self.user)
        # Associate the user group 2 = supplier to the user
        self.user.groups.add(2)
        # Create some Product objects for the supplier
        self.product1 = Product.objects.create(name='Product1', supplier=self.supplier,
                                               product_code='P001', price=100)
        self.product2 = Product.objects.create(name='Product2', supplier=self.supplier,
                                               product_code='P002', price=150)

        # Create cheaper analogues from different suppliers
        self.other_supplier = Supplier.objects.create(
            user=User.objects.create_user(username='otheruser', password='password'))
        self.cheaper_product = Product.objects.create(name='CheaperProduct1',
                                                      supplier=self.other_supplier,
                                                      product_code='P001', price=90)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('supplier_dashboard'))
        self.assertRedirects(response, '/login/?next=/supplier/')

    def test_redirect_if_not_supplier(self):
        # Create a new user not in Supplier group
        non_supplier_user = User.objects.create_user(username='non_supplier',
                                                     password='password')
        self.client.login(username='non_supplier', password='password')
        response = self.client.get(reverse('supplier_dashboard'))
        self.assertRedirects(response, reverse('home'))

    def test_supplier_dashboard_access(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('supplier_dashboard'), follow=True)

        # Check if the user gets the correct template
        self.assertTemplateUsed(response, 'products_store/supplier_dashboard.html')

        # # Check if products and cheaper_analogues are in the context
        self.assertIn('products', response.context)
        self.assertIn('cheaper_analogues', response.context)

        # # Verify that the cheaper analogue is returned in the context
        self.assertEqual(len(response.context['cheaper_analogues']), 1)
        self.assertEqual(response.context['cheaper_analogues'][0], self.cheaper_product)
