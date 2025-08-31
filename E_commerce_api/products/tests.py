from django.test import TestCase

# Create your tests here.


# products/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Product

class ProductTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin", password="pass12345", is_staff=True
        )
        self.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_public_can_list_products(self):
        url = reverse("product-list")   # from router
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_staff_can_create_product(self):
        # get JWT
        url = reverse("token_obtain_pair")
        res = self.client.post(url, {"username": "admin", "password": "pass12345"}, format="json")
        token = res.data["access"]

        # try creating product
        url = reverse("product-list")
        payload = {
            "name": "Wireless Mouse",
            "price": "19.99",
            "category_id": self.category.id,
            "stock_quantity": 10,
        }
        res = self.client.post(url, payload, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
