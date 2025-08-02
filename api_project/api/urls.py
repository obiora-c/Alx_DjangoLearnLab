
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    # Routes for full CRUD via ViewSet
    path('', include(router.urls)),
]
