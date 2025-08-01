from django.db import models

# Create your models here.
# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff') or not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username








# app/models.py
# advanced_features_and_security/models.py

# LibraryProject/bookshelf/models.py

# LibraryProject/bookshelf/models.py

from django.db import models
from django.conf import settings  # ✅ Correct import

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use dynamic user model
        on_delete=models.CASCADE
    )
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
