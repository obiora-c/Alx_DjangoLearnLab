from django.db import models

# Create your models here.
# Create your models here.
class Author(models.Model):
    
    """
    The Author model stores the name of the author.
    Each author can have multiple books associated with them (One-to-Many relationship).
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    
    """
    The Book model stores information about books.
    Each book is linked to a single Author using a foreign key.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books' , on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
