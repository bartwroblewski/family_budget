from django.urls import path

from . import views

urlpatterns = [
    path('budgets/', views.BudgetList.as_view()),
    path('payments/', views.PaymentList.as_view()),
]