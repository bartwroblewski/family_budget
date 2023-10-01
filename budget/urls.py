from django.urls import path

from . import views

urlpatterns = [
    path('budgets/', views.BudgetList.as_view(), name='budgets'),
    path('payments/', views.PaymentList.as_view(), name='payments'),
    path('budget-shares/', views.BudgetShareList.as_view(), name='budget-shares'),
]