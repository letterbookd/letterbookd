from django import forms
from reader.models import Reader, ReaderPreferences

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['display_name', 'bio']

class ReaderPreferencesForm(forms.ModelForm):
    class Meta:
        model = ReaderPreferences
        fields = ['share_reviews', 'share_library']

class UserProfileForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True})
    )
    display_name = forms.CharField(
        label="Display Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Display Name", "id": "display_name"})
    )
    bio = forms.CharField(
        label="Bio",
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Bio", "rows": "2", "id": "bio"})
    )
    share_reviews = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "inputShareReviewPreference"})
    )
    share_library = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "inputShareLibraryPreference"})
    )

    class Meta:
        model = Reader
        fields = ['username', 'display_name', 'bio', 'share_reviews', 'share_library']
