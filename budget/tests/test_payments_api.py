from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from budget.models import Budget, Payment
from .utils import WithLoggedInUserApiTestCase


class PaymentsTestCase(WithLoggedInUserApiTestCase):
    url = reverse('payments')

    def test_user_cannot_add_payment_to_non_existent_budget(self):
        payment = {
            "amount": 100.0,
            "category": "salary",
            "budget": 1
        },
        response = self.client.post(self.url, payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_add_payment_to_budget_he_does_not_own(self):
        other_user = User.objects.create(
            username='other_user', email='other_user@gmail.com')
        other_user_budget = Budget.objects.create(user=other_user)
        payment = {
            "amount": 100.0,
            "category": "salary",
            "budget": other_user_budget.pk,
        }
        response = self.client.post(self.url, data=payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_add_payment_to_budget(self): 
        budget = Budget.objects.create(user=self.user)
        payment = {
            "amount": 100.0,
            "category": "salary",
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.first().budget, budget)

    def test_user_can_add_multiple_payments_to_budget(self): 
        budget = Budget.objects.create(user=self.user)
        payment1 = {
            "amount": 100.0,
            "category": "salary",
            "budget": budget.pk,
        }
        payment2 = {
            "amount": 300.0,
            "category": "salary",
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=payment1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, data=payment2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Payment.objects.count(), 2)
        self.assertEqual(Payment.objects.first().budget, budget)
        self.assertEqual(Payment.objects.all()[1].budget, budget)

    def test_positive_payment_amount_gets_tagged_as_income(self): 
        budget = Budget.objects.create(user=self.user)
        payment = {
            "amount": 100.0,
            "category": "salary",
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=payment, format='json')
        self.assertTrue(response.data['is_income'])

    def test_negative_payment_amount_gets_tagged_as_expense(self): 
        budget = Budget.objects.create(user=self.user)
        payment = {
            "amount": -100.0,
            "category": "salary",
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=payment, format='json')
        self.assertFalse(response.data['is_income'])
        
    def test_payment_amount_cannot_be_0(self):
        budget = Budget.objects.create(user=self.user)
        payment = {
            "amount": 0,
            "category": "salary",
            "budget": budget.pk,
        }
        response = self.client.post(self.url, data=payment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
