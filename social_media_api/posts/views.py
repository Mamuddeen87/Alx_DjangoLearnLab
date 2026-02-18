from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You already liked this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=request.user, post=post)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id
            )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post)

        if not like.exists():
            return Response({"detail": "You have not liked this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)

