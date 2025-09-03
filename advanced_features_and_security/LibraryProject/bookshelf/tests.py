from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
User = get_user_model()
from django.urls import reverse
from .models import Article

class PermissionTestCase(TestCase):
    def setUp(self):
        # Create article
        self.article = Article.objects.create(title="Test", content="Test content", author=self._create_user('author'))

        # Create users and groups
        self.viewer = self._create_user('viewer')
        self.editor = self._create_user('editor')
        self.admin = self._create_user('admin')

        self._assign_permissions()

        self.client = Client()

    def _create_user(self, username):
        return User.objects.create_user(username=username, password='pass1234')
    

    
    def _assign_permissions(self):
        # Get permissions
        perms = {
            'can_view': Permission.objects.get(codename='can_view'),
            'can_create': Permission.objects.get(codename='can_create'),
            'can_edit': Permission.objects.get(codename='can_edit'),
            'can_delete': Permission.objects.get(codename='can_delete'),
        }

        # Groups
        viewers = Group.objects.create(name='Viewers')
        viewers.permissions.add(perms['can_view'])

        editors = Group.objects.create(name='Editors')
        editors.permissions.add(perms['can_view'], perms['can_create'], perms['can_edit'])

        admins = Group.objects.create(name='Admins')
        admins.permissions.add(perms['can_view'], perms['can_create'], perms['can_edit'], perms['can_delete'])

        # Assign users to groups
        self.viewer.groups.add(viewers)
        self.editor.groups.add(editors)
        self.admin.groups.add(admins)

    def test_viewer_can_view(self):
        self.client.login(username='viewer', password='pass1234')
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

    def test_viewer_cannot_create(self):
        self.client.login(username='viewer', password='pass1234')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 403)

    def test_editor_can_create(self):
        self.client.login(username='editor', password='pass1234')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 200)

    def test_editor_cannot_delete(self):
        self.client.login(username='editor', password='pass1234')
        response = self.client.get(reverse('article_delete', args=[self.article.id]))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete(self):
        self.client.login(username='admin', password='pass1234')
        response = self.client.get(reverse('article_delete', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
