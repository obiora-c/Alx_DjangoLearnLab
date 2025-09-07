

from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_id',
            'stock_quantity', 'image_url', 'created_date', 'updated_date'
        ]
        read_only_fields = ['created_date', 'updated_date']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError("Price is required.")
        if value < 0:
            raise serializers.ValidationError("Price must be non-negative.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)
    
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_active']
        read_only_fields = ['id', 'is_staff', 'is_active']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


