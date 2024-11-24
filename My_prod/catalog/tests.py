from rest_framework.test import APITestCase
from rest_framework import status
from catalog.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CatalogAPITestCase(APITestCase):
    def setUp(self):
        # Создаём пользователя и аутентифицируем
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)  # Аутентифицируем клиента

        # Создаём тестовые данные
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            category=self.category,
            price=500.00,
            stock=10,
            description="A test smartphone"
        )

        # URL-ы для тестов
        self.product_list_url = '/api/catalog/products/'
        self.product_detail_url = f'/api/catalog/products/{self.product.id}/'

    def test_get_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_product_detail(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphone")