from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Fetch all book instances from the database
    context = {'books': books}  # Create a context dictionary to pass to the template
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' # This ensures the template uses 'library' as the variable name
