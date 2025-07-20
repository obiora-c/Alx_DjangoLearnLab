from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # <-- REQUIRED EXPLICITLY
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

 
 
 
 
 
 # views.py
# relationship_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('home')  # Replace 'home' with your actual landing page name
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})



from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# relationship_app/views.py

# LibraryProject/relationship_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required  # ✅ Add this line
from .models import Book
from .forms import BookForm  # Ensure you have a BookForm defined

# ✅ View to add a book — requires 'can_add_book' permission
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

# ✅ View to edit a book — requires 'can_change_book' permission
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

# ✅ View to delete a book — requires 'can_delete_book' permission
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
