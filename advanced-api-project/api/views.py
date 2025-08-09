from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books
class BookListView(generics.ListAPIView):
    
    
    """
    Returns a list of all books in the database.
    Accessible to both authenticated and unauthenticated users.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
# Retrieve a single book by ID  
class BookDetailView(generics.RetrieveAPIView):
    
    """
    Retrieves a single book based on its primary key.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
 
    
# Create a new book
class BookCreateView(generics.CreateAPIView):
    
    
    """
    Allows an authenticated user to create a book.
    """   
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Example: log creation or associate with request.user if needed
        serializer.save()
 
 

# Update an existing book   
class  BookUpdateView(generics.CreateAPIView):
    
    """
    Allows an authenticated user to update a book.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]
     
    