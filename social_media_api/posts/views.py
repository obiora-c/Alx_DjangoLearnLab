from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Custom permission: only allow owners to edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get users the current user follows
        following_qs = self.request.user.following.all()
        # Return posts from those users, newest first
        return Post.objects.filter(author__in=following_qs).order_by('-created_at')
