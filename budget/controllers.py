from .models import Budget

def get_user_budgets(user):
    user_budgets = Budget.objects.filter(user=user)
    budgets_shared_with_user = Budget.objects \
        .select_related('budget_share') \
        .filter(budgetshare__shared_with=user)
    return user_budgets | budgets_shared_with_user