from django.forms import ModelForm
from reader.models import Reader, ReaderPreferences

class ReaderForm(ModelForm):
    class Meta:
        model = Reader
        fields = ['display_name', 'bio', 'profile_picture', 'personal_library']

class ReaderPreferencesForm(ModelForm):
    class Meta:
        model = ReaderPreferences
        fields = ['share_reviews', 'share_library']
