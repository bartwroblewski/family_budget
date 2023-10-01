from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.user_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': '123!@aiourlgn45',
        }

    def test_user_can_register(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user1')

    def test_user_cannot_register_if_email_is_invalid(self):
        self.user_data['email'] = 'user1gmail.com'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_if_password_is_too_easy(self):
        self.user_data['password'] = 'password'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)