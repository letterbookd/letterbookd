from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from library.models import LibraryBook

class LibraryBookForm(ModelForm):
    class Meta:
        model = LibraryBook
        exclude = ['library']
        fields = ["book", "tracking_status", "is_favorited"]
        widgets = {
            "book": forms.Select(attrs={'class': 'form-select'}),
            "tracking_status": forms.Select(attrs={'class': 'form-select'}),
            "is_favorited": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UpdateLibBookForm(ModelForm):
    class Meta:
        model = LibraryBook
        exclude = ['library', 'book']
        fields = ["tracking_status", "is_favorited"]
        widgets = {
            "tracking_status": forms.Select(attrs={'class': 'form-select'}),
            "is_favorited": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
