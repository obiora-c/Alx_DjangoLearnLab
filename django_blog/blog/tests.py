from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.other  = User.objects.create_user(username="other",  password="pass12345")
        self.post = Post.objects.create(title="Hello", content="World", author=self.author)

    def test_list_and_detail_accessible_to_all(self):
        resp = self.client.get(reverse("post-list"))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse("post-detail", args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse("post-create"))
        self.assertEqual(resp.status_code, 302)  # redirect to login

        self.client.login(username="author", password="pass12345")
        resp = self.client.post(reverse("post-create"), {"title": "New", "content": "Body"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New", author=self.author).exists())

    def test_only_author_can_edit(self):
        self.client.login(username="other", password="pass12345")
        resp = self.client.get(reverse("post-edit", args=[self.post.pk]))
        self.assertIn(resp.status_code, [302, 403])  # depending on raise_exception

        self.client.logout()
        self.client.login(username="author", password="pass12345")
        resp = self.client.post(reverse("post-edit", args=[self.post.pk]), {"title": "Edited", "content": "Body"})
        self.assertEqual(resp.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Edited")

    def test_only_author_can_delete(self):
        self.client.login(username="other", password="pass12345")
        resp = self.client.post(reverse("post-delete", args=[self.post.pk]))
        self.assertIn(resp.status_code, [302, 403])
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

        self.client.logout()
        self.client.login(username="author", password="pass12345")
        resp = self.client.post(reverse("post-delete", args=[self.post.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
