from django.forms import ModelForm
from review.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["stars_rating", "status_on_review", "review_text"]