from .models import Budget, BudgetShare, Payment
from .serializers import BudgetSerializer, PaymentSerializer

def get_user_budgets(user):
    budgets = []
    for budget in Budget.objects.filter(user=user):
        # TODO: address N+1 problem here
        payments = Payment.objects.filter(budget=budget)
        income = []
        expenses = []
        for payment in payments:
            # TODO custom queryset managers on Payment model instead (Payment.income, Payment.expenses)
            if payment.amount > 0:
                income.append(PaymentSerializer(payment).data)
            elif payment.amount < 0:
                expenses.append(PaymentSerializer(payment).data)
        budget_dict = {
            'payments': {
                'income': income,
                'expenses': expenses,
            }
        }
        budgets.append(budget_dict)
    return budgets

def get_budgets_shared_with_user(user):
    # TODO express this better and faster via ORM api
    return [
        BudgetSerializer(share.budget).data
        for share in BudgetShare.objects.filter(shared_with=user)
    ]