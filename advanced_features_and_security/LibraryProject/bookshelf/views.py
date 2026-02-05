from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book  # or CustomUser if needed
from .forms import ExampleForm  # <-- add this line

# List of books view
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Optional: Example view to use the form
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # or your URL name
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

