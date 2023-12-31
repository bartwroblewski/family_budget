from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

class WithLoggedInUserApiTestCase(APITestCase):
    def get_user(self, username, email, password):
        user_data = {'username': username, 'email': email, 'password': password}
        self.client.post(reverse('register'), user_data, format='json')
        self.client.login(username=username, password=password)
        return User.objects.get(username=username)

    def setUp(self):
        self.user = self.get_user('user1', 'user1@gmail.com', '123jgj@#jg55%$')