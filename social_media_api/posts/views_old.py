from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Post, Like
from notifications.models import Notification

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only owners can edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the author
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content'] 
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
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

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class FeedView(APIView):
    """
    Returns posts from users the current user follows,
    ordered by newest first.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get users the current user is following
        following_users = request.user.following.all()

        # Get posts from those users ordered by newest first
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Like.objects.create(user=request.user, post=post)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post"
            )

        return Response({"detail": "Post liked successfully."}, status=201)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post)

        if not like.exists():
            return Response(
                {"detail": "You have not liked this post."},
                status=400
            )

        like.delete()

        return Response({"detail": "Post unliked successfully."}, status=200)

