from rest_framework.test import APITestCase
from rest_framework import status
from catalog.models import Product
from orders.models import Cart, CartItem, Order, Contact
from django.contrib.auth import get_user_model
from catalog.models import Category


User = get_user_model()


class CartAPITestCase(APITestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

        # Создаём категорию для товара
        self.category = Category.objects.create(name="Electronics")

        # Создаём тестовый продукт с категорией
        self.product = Product.objects.create(
            name="Smartphone",
            category=self.category,  # Указываем категорию
            price=500.00,
            stock=10,
            description="Test smartphone"
        )

        # URL для работы с корзиной
        self.cart_url = '/api/orders/cart/'

    def test_add_to_cart(self):
        data = {"product_id": self.product.id, "quantity": 1}
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, 200)

    def test_get_cart(self):
        Cart.objects.create(user=self.user)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

        # Создаём контакт
        self.contact = Contact.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="+123456789",
            city="City",
            street="Street",
            house="123"
        )

        # Создаём категорию для продукта
        self.category = Category.objects.create(name="Electronics")

        # Создаём продукт с категорией
        self.product = Product.objects.create(
            name="Smartphone",
            category=self.category,  # Указываем категорию
            price=500.00,
            stock=10
        )

        # Создаём корзину
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        # URL для подтверждения заказа
        self.order_url = '/api/orders/confirm/'

    def test_confirm_order(self):
        data = {"contact_id": self.contact.id}
        response = self.client.post(self.order_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)