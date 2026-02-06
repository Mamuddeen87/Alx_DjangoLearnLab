from django.urls import path, include
from .views import BookViewSet
from .views import BookList
from rest_framework.routers import DefaultRouter

# Step 1: create the router
router = DefaultRouter()

# Step 2: register the ViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

# Step 3: define urlpatterns
urlpatterns = [
    # Keep your ListAPIView if you still want it
    path('books/', BookList.as_view(), name='book-list'),

    # Include all routes from the router (CRUD)
    path('', include(router.urls)),
]

