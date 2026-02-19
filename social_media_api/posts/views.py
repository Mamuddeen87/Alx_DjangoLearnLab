from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from django.contrib.auth import get_user_model


User = get_user_model()
# -----------------------------
# POST CRUD
# -----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Only author can update
        if self.get_object().author != self.request.user:
            raise PermissionError("You cannot edit someone else's post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError("You cannot delete someone else's post.")
        instance.delete()


# -----------------------------
# COMMENT CRUD
# -----------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # Create notification for post author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                content_type=ContentType.objects.get_for_model(comment.post),
                object_id=comment.post.id
            )

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionError("You cannot edit someone else's comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError("You cannot delete someone else's comment.")
        instance.delete()


# -----------------------------
# FEED
# -----------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users that current user follows
        following_users = self.request.user.following.all()
        # Posts from those users, newest first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


# -----------------------------
# LIKE / UNLIKE
# -----------------------------
class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Get the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Create like if it doesn't exist
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        # If like was newly created, create notification
        if created and post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response(
            {"message": "Post liked"},
            status=status.HTTP_201_CREATED
        )
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if like:
            like.delete()

        return Response(
            {"message": "Post unliked"},
            status=status.HTTP_200_OK
        )

