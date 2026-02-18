from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView
from .views import LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = router.urls + [
    path("feed/", FeedView.as_view(), name="feed"),
    path("like/<int:post_id>/", LikePostView.as_view(), name="like-post"),
    path("unlike/<int:post_id>/", UnlikePostView.as_view(), name="unlike-post"),
]

