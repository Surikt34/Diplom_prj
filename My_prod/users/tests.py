from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            phone="+1234567890",
        )
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')

    def test_register_user(self):
        """Тест регистрации пользователя"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "phone": "+1234567890",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username="newuser").email, "newuser@example.com")

    def test_register_with_existing_email(self):
        """Тест регистрации с уже существующим email"""
        data = {
            "username": "newuser",
            "email": "testuser@example.com",  # Используем email уже существующего пользователя
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_with_existing_username(self):
        """Тест регистрации с уже существующим именем пользователя"""
        data = {
            "username": "testuser",  # Используем username уже существующего пользователя
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_get_user_profile(self):
        """Тест получения профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        """Тест обновления профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.patch(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")