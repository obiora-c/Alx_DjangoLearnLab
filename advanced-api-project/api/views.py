from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# List all books
class BookListView(generics.ListAPIView):
    
    
    """
    BookListView:
    - Supports:
    • Filtering by title, author (ID), and publication_year via query params.
    • Search by title and author's name using `search=` query param.
    • Ordering by title, publication_year, or author using `ordering=` param.
    Examples:
    - /api/books/?publication_year=2020
    - /api/books/?search=Orwell
    - /api/books/?ordering=-publication_year
    """

    
    
    """
    Returns a list of all books in the database.
    Accessible to both authenticated and unauthenticated users.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    # Add filtering, search, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filter by fields
    filterset_fields = ['title', 'publication_year', 'author']
    
    # Search in title and author's name (requires nested lookup)
    search_fields = ['title', 'author__name']
    
    # Allow ordering by any field
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']  # Default ordering
 
    
# Retrieve a single book by ID  
class BookDetailView(generics.RetrieveAPIView):
    
    """
    Retrieves a single book based on its primary key.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    

    
# Create a new book
class BookCreateView(generics.CreateAPIView):
    
    
    """
    Allows an authenticated user to create a book.
    """   
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        # Example: log creation or associate with request.user if needed
        serializer.save()
 
 

# Update an existing book   
class  BookUpdateView(generics.UpdateAPIView):
    
    """
    Allows an authenticated user to update a book.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        # Example: log creation or associate with request.user if needed
        serializer.save()
     
     
# Delete a book     
class  BookDeleteView(generics.DestroyAPIView):

    """
    Allows an authenticated user to delete a book.
    """
  
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
     
    