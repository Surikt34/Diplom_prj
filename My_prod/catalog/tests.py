from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product

class CatalogAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.category = Category.objects.create(name="Электроника")
        self.product = Product.objects.create(
            name="Смартфон",
            category=self.category,
            price=1000,
            stock=50,
            description="Тестовый смартфон"
        )

    def test_category_list(self):
        response = self.client.get('/api/catalog/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_product_detail(self):
        response = self.client.get(f'/api/catalog/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Смартфон")