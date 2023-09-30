from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .controllers import get_user_budgets, get_budgets_shared_with_user
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

class BudgetList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        entries = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        entries = Payment.objects.all()
        serializer = PaymentSerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BudgetShareList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        entries = BudgetShare.objects.all()
        serializer = BudgetShareSerializer(entries, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        # TODO: maybe add validation here (or in models? serializers?) to check
        # if budget being shared is in user's possesion
        serializer = BudgetShareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO better class name and better url path (users/id/budgets?)
class UserBudgets(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        budgets = get_user_budgets(request.user)        
        return Response({
            'budgets': budgets, 
            'shared_budgets': get_budgets_shared_with_user(request.user),
        }) 