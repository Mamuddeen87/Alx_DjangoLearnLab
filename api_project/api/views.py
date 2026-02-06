from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Book
from rest_framework import viewsets
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    #this provides full CRUD operations for Book Model.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
