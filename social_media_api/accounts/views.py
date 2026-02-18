from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

User = get_user_model()

class FollowUserView(generics.GenericAPIView):
    """
    Allows authenticated users to follow another user.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(CustomUser, username=username)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        if user_to_follow != request.user:
            Notification.objects.create(
                    recipient=user_to_follow,
                    actor=request.user,
                    verb="started following you",
                    content_type=ContentType.objects.get_for_model(user_to_follow),
                    object_id=user_to_follow.id
                    )

        return Response(
            {"detail": f"You are now following {username}."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows authenticated users to unfollow another user.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        user_to_unfollow = get_object_or_404(CustomUser, username=username)

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"detail": f"You have unfollowed {username}."},
            status=status.HTTP_200_OK
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "followers_count": user.followers.count(),
            "following_count": user.following.count(),
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({
            "token": token.key,
            "user_id": token.user_id,
            "username": token.user.username,
        })

