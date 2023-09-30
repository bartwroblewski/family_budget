from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_non_zero(amount: float):
    if amount == 0:
        raise ValidationError('Budget amount cannot be 0.')

class BudgetEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(validators=[validate_non_zero])
    category = models.CharField(max_length=100)