from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from budget.models import Budget, BudgetShare
from .utils import WithLoggedInUserApiTestCase


class BudgetSharesTestCase(WithLoggedInUserApiTestCase):
    url = reverse('budget-shares')

    def test_user_cannot_share_budget_he_does_not_own(self):
        other_user = User.objects.create(
            username='other_user', email='other_user@gmail.com')
        other_user_budget = Budget.objects.create(user=other_user)
        share = {
            "shared_with": other_user.pk,
            "budget": other_user_budget.pk,
        }
        response = self.client.post(self.url, data=share, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_share_budget_with_himself(self):
        budget = Budget.objects.create(user=self.user)
        share = {
            "shared_with": self.user.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_share_budget(self):
        other_user = User.objects.create(
            username='other_user', email='other_user@gmail.com')
        budget = Budget.objects.create(user=self.user)
        share = {
            "shared_with": other_user.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(BudgetShare.objects.count(), 1)
        budget_share = BudgetShare.objects.get()
        self.assertEqual(budget_share.shared_by, self.user)
        self.assertEqual(budget_share.shared_with, other_user)
        self.assertEqual(budget_share.budget, budget)

    def test_user_can_share_same_budget_to_multiple_users(self):
        other_user1 = User.objects.create(
            username='other_user1', email='other_user1@gmail.com')
        other_user2 = User.objects.create(
            username='other_user2', email='other_user2@gmail.com')
        budget = Budget.objects.create(user=self.user)

        share1 = {
            "shared_with": other_user1.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        share2 = {
            "shared_with": other_user2.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        budget_shares = BudgetShare.objects.all()
        self.assertEqual(budget_shares.count(), 2)
        self.assertEqual(budget_shares.first().shared_by, self.user)
        self.assertEqual(budget_shares.first().shared_with, other_user1)
        self.assertEqual(budget_shares.first().budget, budget)
        self.assertEqual(budget_shares[1].shared_by, self.user)
        self.assertEqual(budget_shares[1].shared_with, other_user2)
        self.assertEqual(budget_shares[1].budget, budget)

    def test_user_can_share_same_budget_to_same_user_more_than_once(self):
        other_user = User.objects.create(
            username='other_user', email='other_user@gmail.com')
        budget = Budget.objects.create(user=self.user)

        share1 = {
            "shared_with": other_user.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        share2 = {
            "shared_with": other_user.pk,
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=share2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        budget_shares = BudgetShare.objects.all()
        self.assertEqual(budget_shares.count(), 2)
        self.assertEqual(budget_shares.first().shared_by, self.user)
        self.assertEqual(budget_shares.first().shared_with, other_user)
        self.assertEqual(budget_shares.first().budget, budget)
        self.assertEqual(budget_shares[1].shared_by, self.user)
        self.assertEqual(budget_shares[1].shared_with, other_user)
        self.assertEqual(budget_shares[1].budget, budget)

       