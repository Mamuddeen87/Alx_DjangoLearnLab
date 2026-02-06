from django.urls import path, include
from .views import BookViewSet
from .views import BookList
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Step 1: create the router
router = DefaultRouter()

# Step 2: register the ViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

# Step 3: define urlpatterns
urlpatterns = [
    # Keep your ListAPIView if you still want it
    path('books/', BookList.as_view(), name='book-list'),

    #token authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Include all routes from the router (CRUD)
    path('', include(router.urls)),
]

