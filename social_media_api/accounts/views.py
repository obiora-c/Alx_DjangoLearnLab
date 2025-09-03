from django.shortcuts import render

# Create your views here.



from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import PublicUserSerializer
from .models import CustomUser


CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=target.id).exists():
            return Response({"detail": "Already following."}, status=status.HTTP_200_OK)

        request.user.following.add(target)
        data = {
            "detail": f"You are now following {target.username}.",
            "you": PublicUserSerializer(request.user).data,
            "target": PublicUserSerializer(target).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(id=target.id).exists():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_200_OK)

        request.user.following.remove(target)
        data = {
            "detail": f"You unfollowed {target.username}.",
            "you": PublicUserSerializer(request.user).data,
            "target": PublicUserSerializer(target).data,
        }
        return Response(data, status=status.HTTP_200_OK)