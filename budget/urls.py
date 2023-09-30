from django.urls import path

from . import views

urlpatterns = [
    path('budgets/', views.BudgetList.as_view()),
    path('payments/', views.PaymentList.as_view()),
    path('budget-shares/', views.BudgetShareList.as_view()),
    path('user-budgets/', views.UserBudgets.as_view()),
]