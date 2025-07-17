

import os
import sys
import django

# Setup Django environment
sys.path.append("C:/Users/USER/Alx_DjangoLearnLab/django-models/LibraryProject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Example data creation
    author = Author.objects.create(name='George Orwell')
    book1 = Book.objects.create(title='1984', author=author)
    book2 = Book.objects.create(title='Animal Farm', author=author)
    
    library = Library.objects.create(name='Central Library')
    library.books.add(book1, book2)
    
    librarian = Librarian.objects.create(name='Alice Johnson', library=library)

    # 1. Query all books by a specific author
    books_by_orwell = Book.objects.filter(author__name='George Orwell')
    print("Books by George Orwell:")
    for book in books_by_orwell:
        print(f" - {book.title}")

    # 2. List all books in a library
    library_books = library.books.all()
    print("\nBooks in Central Library:")
    for book in library_books:
        print(f" - {book.title}")

    # 3. Retrieve the librarian for a library
    lib_librarian = library.librarian
    print(f"\nLibrarian of Central Library: {lib_librarian.name}")


