from django.urls import path
from .views import list_books, LibraryDetailView
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    list_books,
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    register,
)

urlpatterns = [
    # Existing views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Role-based views
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
]

urlpatterns = [
    # Route for the function-based view
    path('books/', list_books, name='list_books'),
    
    # Route for the class-based view
    # <int:pk> is a placeholder for the Library's primary key
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ... your existing book/library URLs ...

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
