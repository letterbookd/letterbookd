from django.db import models
from library.models import *
from reader.models import *
from catalog.models import *

# TODO
class Review(models.Model):
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    stars_rating = models.FloatField()
    status_on_review = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    review_text = models.TextField()