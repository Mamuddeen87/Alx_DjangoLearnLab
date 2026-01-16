from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Route for the function-based view
    path('books/', list_books, name='list_books'),
    
    # Route for the class-based view
    # <int:pk> is a placeholder for the Library's primary key
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('', include('relationship_app.urls')),
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
