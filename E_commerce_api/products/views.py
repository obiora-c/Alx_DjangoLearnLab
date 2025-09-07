from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets, permissions


from .permissions import IsAdminOrReadOnly
permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'price': ['exact', 'gte', 'lte'],
        'category__id': ['exact'],
        'stock_quantity': ['gte', 'lte'],
    }
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_date', 'name']

    # Example custom endpoint to decrement stock (optional)
    @action(detail=True, methods=['post'])
    def reduce_stock(self, request, pk=None):
        product = self.get_object()
        qty = int(request.data.get('quantity', 1))
        try:
            product.reduce_stock(qty)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'id': product.id, 'stock_quantity': product.stock_quantity})

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'slug']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =  [permissions.IsAdminUser]  # Only admin can CRUD users # [permissions.AllowAny]  # For registration      [permissions.IsAdminUser]  # Only admin can CRUD users