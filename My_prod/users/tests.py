from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/login/'

    def test_user_registration(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)

    def test_user_login(self):
        user = User.objects.create_user(email="testuser@example.com", password="password123")
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_with_invalid_credentials(self):
        data = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)