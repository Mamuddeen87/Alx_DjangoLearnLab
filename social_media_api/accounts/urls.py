from django.urls import path, include
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("follow/<str:username>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<str:username>/", UnfollowUserView.as_view(), name="unfollow-user"),
]

