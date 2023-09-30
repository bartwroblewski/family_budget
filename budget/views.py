from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BudgetEntrySerializer, RegisterUserSerializer, UserSerializer
from .models import BudgetEntry


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (permissions.AllowAny,)
  serializer_class = RegisterUserSerializer

class BudgetEntryList(APIView):

    def get(self, request, format=None):
        entries = BudgetEntry.objects.all()
        serializer = BudgetEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BudgetEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

