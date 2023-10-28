from django import forms
from .models import Thread, Reply
from django.forms.utils import ErrorList

class ThreadForm(forms.ModelForm):
    title = forms.CharField(
        label='Thread Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the thread title',
        })
    )
    content = forms.CharField(
        label='Thread Content',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the thread content',
        })
    )

    class Meta:
        model = Thread
        fields = ['title', 'content']


class RepliesForm(forms.ModelForm):
    content = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your reply message',
            'rows': '4'
        })
    )

    class Meta:
        model = Reply
        fields = ['content']


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger alert-dismissible fade show d-flex align-items-center"><i class="bi bi-exclamation-triangle-fill me-2"></i><div>%s</div><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>' % e for e in self])
