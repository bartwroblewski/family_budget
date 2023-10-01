from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .controllers import get_budgets_shared_with_user, get_user_budgets
from .serializers import (
    BudgetSerializer,
    BudgetShareSerializer,
    PaymentSerializer,
    RegisterUserSerializer,
    UserSerializer,
)
from .models import Budget, BudgetShare, Payment


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
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        user_budgets = Budget.objects.filter(user=self.request.user)
        return Payment.objects.filter(budget__in=user_budgets)
    
    def perform_create(self, serializer):
        user_budgets = Budget.objects.filter(user=self.request.user)
        budget = serializer.validated_data['budget']
        if budget not in user_budgets:
            raise exceptions.PermissionDenied(
                "You cannot add payments to budgets you don't own")
        serializer.save()
    
class BudgetShareList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BudgetShareSerializer
    queryset = BudgetShare.objects.all()

    # TODO: maybe add validation here (or in models? serializers?) to check
    # if budget being shared is in user's possesion

# TODO better class name and better url path (users/id/budgets?)
class UserBudgets(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        budgets = get_user_budgets(request.user)        
        return Response({
            'budgets': budgets, 
            # TODO:shared budgets should rather be a separate endpoint
            'shared_budgets': get_budgets_shared_with_user(request.user),
        }) 