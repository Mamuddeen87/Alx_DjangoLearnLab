from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):  # <-- renamed to ExampleForm
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']  # adjust fields as needed

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title


