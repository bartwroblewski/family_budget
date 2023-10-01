from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from budget.models import Budget

class BudgetsTestCase(APITestCase):
    def get_user(self, username, email, password):
        user_data = {'username': username, 'email': email, 'password': password}
        self.client.post(reverse('register'), user_data, format='json')
        self.client.login(username=username, password=password)
        return User.objects.first()

    def setUp(self):
        self.user = self.get_user('user1', 'user1@gmail.com', '123jgj@#jg55%$')
        self.url = reverse('budgets')

    def test_user_can_add_budget(self): 
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.first().user.pk, self.user.pk)

    def test_user_can_add_multiple_budgets(self): 
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.first().user.pk, self.user.pk)

        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 2)
        self.assertEqual(Budget.objects.all()[1].user.pk, self.user.pk)
