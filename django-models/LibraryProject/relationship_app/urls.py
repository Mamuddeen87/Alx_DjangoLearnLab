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
