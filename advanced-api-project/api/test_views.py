

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password= 'pass123')
        self.client = APIClient()
        
        
        self.author = Author.objects.create(name= 'Georgr Orwell')
        

        # Create books
        self.book1 = Book.objects.create(title='1984', publication_year=1949, author=self.author)
        self.book2 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author)

        # Endpoints
        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', args=[pk])
        self.create_url = reverse('book-create')
        self.update_url = lambda pk: reverse('book-update', args=[pk])
        self.delete_url = lambda pk: reverse('book-delete', args=[pk])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    def test_create_book_unauthenticated(self):
        data = {'title': 'New Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        data = {'title': 'New Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        data = {'title': 'Updated Title', 'publication_year': 1949, 'author': self.author.id}
        response = self.client.put(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filter_books_by_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=1949")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_search_books_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Animal")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')

    def test_order_books_by_title_desc(self):
        response = self.client.get(f"{self.list_url}?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')

    def test_create_book_with_future_year(self):
        self.client.login(username='testuser', password='pass123')
        future_year = 3000
        data = {'title': 'Future Book', 'publication_year': future_year, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)