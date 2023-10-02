from .models import Budget, BudgetShare

def get_user_budgets(user):
    user_budgets = Budget.objects.filter(user=user)
    budgets_shared_with_user = Budget.objects.filter(pk__in=(
        share.budget.pk
        for share in BudgetShare.objects.filter(shared_with=user)
    ))
    return user_budgets | budgets_shared_with_user