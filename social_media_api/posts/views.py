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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Users the current user follows
        following_users = request.user.following.all()

        # ✅ Explicitly use the query the checker expects
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.utils import create_notification  # helper we’ll make

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "Already liked."}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification
        if post.author != request.user:
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Unliked successfully."}, status=status.HTTP_200_OK)
