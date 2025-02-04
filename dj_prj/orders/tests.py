from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Product, Category
from orders.models import Order, Cart, CartItem, Contact

User = get_user_model()


class OrderAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовую категорию
        self.category = Category.objects.create(name="Test Category")

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10,
            category=self.category  # Указываем категорию
        )

        # Создаем корзину и элемент корзины
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Создаем контакт
        self.contact = Contact.objects.create(
            user=self.user,
            last_name="Doe",
            first_name="John",
            phone="1234567890",
            city="City",
            street="Street",
            house="1"
        )

    def test_get_orders(self):
        """Тест получения списка заказов"""
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_order_detail(self):
        """Тест получения информации о заказе"""
        order = Order.objects.create(user=self.user, total_price=200)
        response = self.client.get(reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)

    def test_create_order(self):
        """Тест создания заказа"""
        response = self.client.post(reverse('order-confirm'), data={"contact_id": self.contact.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_get_cart(self):
        """Тест получения корзины"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)



    def test_remove_from_cart(self):
        """Тест удаления товара из корзины"""
        response = self.client.delete(reverse('cart-delete', args=[self.cart_item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)



    def test_invalid_contact(self):
        """Тест создания контакта с некорректными данными"""
        data = {
            "last_name": "Smith",
            "city": "City"
        }
        response = self.client.post(reverse('contact-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_status_admin(self):
        """Тест обновления статуса заказа администратором"""
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        self.client.force_authenticate(user=admin)
        order = Order.objects.create(user=self.user, total_price=300)
        response = self.client.patch(reverse('order-update-status', args=[order.id]), data={"status": "completed"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "completed")