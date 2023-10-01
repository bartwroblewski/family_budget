from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_non_zero(amount: float):
    if amount == 0:
        raise ValidationError('Budget amount cannot be 0.')
    
class Budget(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Payment(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(validators=[validate_non_zero])
    category = models.CharField(max_length=100)

class BudgetShare(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    shared_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='shared_by_budget_share_set',
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_with_budget_share_set',
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)