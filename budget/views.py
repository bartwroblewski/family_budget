from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, generics, permissions, viewsets

from .controllers import get_user_budgets, get_user_payments
from .serializers import (
    BudgetSerializer,
    BudgetShareSerializer,
    PaymentSerializer,
    RegisterUserSerializer,
    UserSerializer,
)
from .models import BudgetShare, Payment


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterUser(generics.CreateAPIView):
  permission_classes = [permissions.AllowAny]
  serializer_class = RegisterUserSerializer

class BudgetList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return get_user_budgets(self.request.user).order_by(
            'created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return get_user_payments(self.request.user).order_by('created_at')
    
    def perform_create(self, serializer):
        budget = serializer.validated_data['budget']
        if budget.user != self.request.user:
            raise exceptions.PermissionDenied(
                "You cannot add payments to budgets you don't own")
        serializer.save()
    
class BudgetShareList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BudgetShareSerializer

    def get_queryset(self):
        return BudgetShare.objects.filter(
            shared_by=self.request.user).order_by('created_at')
    
    def perform_create(self, serializer):
        budget = serializer.validated_data['budget']
        if budget.user != self.request.user:
            raise exceptions.PermissionDenied(
                "You cannot share budgets you don't own")
        
        shared_with = serializer.validated_data['shared_with']
        if shared_with == budget.user:
            raise exceptions.PermissionDenied(
                "You cannot share budget with yourself")
        
        serializer.save(shared_by=self.request.user)
