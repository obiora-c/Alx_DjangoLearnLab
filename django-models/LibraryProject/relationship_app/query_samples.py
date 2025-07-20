
import os
import sys
import django

# Setup Django environment
sys.path.append("C:/Users/USER/Alx_DjangoLearnLab/django-models/LibraryProject")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# Query: All books in a specific library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)  # ✅ This is the required line
    books_in_library = library.books.all()
    print(f"\nBooks in {library_name}:")
    for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")



# ✅ Query: All books by a specific author (using required code lines)
author_name = "Jane Doe"
try:
    author = Author.objects.get(name=author_name)  # ✅ Required line
    books_by_author = Book.objects.filter(author=author)  # ✅ Required line
    print(f"\nBooks by {author_name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"Author '{author_name}' not found.")



# Query: Retrieve the librarian for a library
try:
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)  # ✅ Required line
    print(f"\nLibrarian of {library_name}: {librarian.name}")
except (Library.DoesNotExist, Librarian.DoesNotExist):
    print(f"No librarian found for library '{library_name}'.")