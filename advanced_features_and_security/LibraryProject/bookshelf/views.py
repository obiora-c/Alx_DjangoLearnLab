from django.shortcuts import render

# Create your views here.



# advanced_features_and_security/views.py

# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})








from django.shortcuts import render
from django.db.models import Q
from .models import MyModel  # Replace with your actual model

def search(request):
    query = request.GET.get('q', '')
    results = MyModel.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})



from django.shortcuts import render
from .models import MyModel  # Replace with your actual model
from .forms import SearchForm  # This should be defined in forms.py

def safe_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            results = MyModel.objects.filter(name__icontains=query)
            return render(request, 'search_results.html', {'results': results, 'form': form})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})




from django.shortcuts import render
from .models import Book
from .forms import SearchForm

def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()
    if form.is_valid():
        title = form.cleaned_data.get('title')
        if title:
            books = books.filter(title__icontains=title)
    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})
