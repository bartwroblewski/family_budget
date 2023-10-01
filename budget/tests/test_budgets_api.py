from django.urls import reverse
from rest_framework import status

from budget.models import Budget
from .utils import WithLoggedInUserApiTestCase


class BudgetsTestCase(WithLoggedInUserApiTestCase):
    url = reverse('budgets')

    def test_user_can_add_budget(self): 
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.first().user, self.user)

    def test_user_can_add_multiple_budgets(self): 
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(Budget.objects.first().user, self.user)

        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 2)
        self.assertEqual(Budget.objects.all()[1].user, self.user)
