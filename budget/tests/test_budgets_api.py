from django.contrib.auth.models import User
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

    def test_if_user_shares_a_budget_with_other_user_the_other_user_can_see_the_budget_in_his_budget_list(self):
        other_user = User.objects.create(
            username='other_user',
            email='other_user@gmail.com',
            password='gg$$%@gg454',
        )
        budget = Budget.objects.create(user=self.user)
        share = {
            "shared_with": other_user.pk,
            "budget": budget.pk,
        }
        self.client.post(reverse('budget-shares'), data=share, format='json')
        self.client.logout()

        self.client.force_login(user=other_user)

        response = self.client.get(reverse('budgets'))
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], budget.pk)
