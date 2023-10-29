from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    isbn13 = models.BigIntegerField()
    title = models.CharField(max_length=225, null=True, blank=True)
    authors = models.CharField(max_length=225, null=True, blank=True)
    categories = models.CharField(max_length=225, null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    overall_rating = models.FloatField(default=0, null=True, blank=True)
    favorites_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"\"{self.title}\" by {self.authors.replace(';', ', ')}"

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"