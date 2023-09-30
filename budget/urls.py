from django.urls import path

from . import views

urlpatterns = [
    path('budget/', views.BudgetEntryList.as_view()),

]