from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Book
from rest_framework import viewsets
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ✅ Requires authentication
    permission_classes = [IsAdminUser]
    

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or obj.owner == request.user
    
    
    
# BookViewSet requires users to be authenticated using token-based auth.
# Users must send their token in the Authorization header as: Token <token>
# This view will reject unauthenticated requests.
