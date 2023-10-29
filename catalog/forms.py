from django.forms import ModelForm
from catalog.models import *

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["isbn13", "title", "authors", "categories", "thumbnail", "description", "published_year", "page_count"]