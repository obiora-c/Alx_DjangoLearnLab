from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # <-- REQUIRED EXPLICITLY
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

 
 