from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser  # Or Book if you have a Book model here
from .models import Book
# Create your views here.

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Query all books
    return render(request, 'bookshelf/book_list.html', {'books': books})


