from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from catalog.models import Category, Product, Supplier

User = get_user_model()

class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Category 1")
        self.url = reverse('category-list')
        cache.clear()

    def test_get_categories_from_cache(self):
        cache.set('category_list', [{"id": self.category.id, "name": self.category.name}])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": self.category.id, "name": self.category.name}])

    def test_get_categories_from_db(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.category.name)

class ProductListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Category 1")
        self.product = Product.objects.create(name="Product 1", category=self.category, price=100.0, stock=10)
        self.url = reverse('product-list')
        cache.clear()

    def test_get_products_from_cache(self):
        cache.set('product_list', [{"id": self.product.id, "name": self.product.name}])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": self.product.id, "name": self.product.name}])

    def test_get_products_from_db(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.product.name)

class SupplierListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.supplier = Supplier.objects.create(name="Supplier 1")
        self.url = reverse('supplier-list')
        cache.clear()

    def test_get_suppliers_from_cache(self):
        cache.set('supplier_list', [{"id": self.supplier.id, "name": self.supplier.name}])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": self.supplier.id, "name": self.supplier.name}])

    def test_get_suppliers_from_db(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.supplier.name)

