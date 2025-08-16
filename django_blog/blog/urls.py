from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView,
)
from .views import  CommentUpdateView, CommentDeleteView, CommentCreateView




urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path("post/",                 PostListView.as_view(),   name="post-list"),
    path("post/new/",             PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/",        PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/",   PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-add"),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

]
