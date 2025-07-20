from django.shortcuts import render

# Create your views here.

 #Function-based View: List All Books
 
 
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})


#Class-based View: Display Library Details

from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'