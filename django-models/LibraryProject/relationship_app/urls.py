

from django.urls import path
from .views import book_list_view, LibraryDetailView

urlpatterns = [
    path('books/', book_list_view, name='book-list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
