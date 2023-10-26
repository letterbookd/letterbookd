from django.db import models
from django.contrib.auth.models import User
from library.models import *
from review.models import *

# TODO ganti kalau butuh
class ReaderPreferences(models.Model):
    share_reviews = models.BooleanField(default=True)
    share_library = models.BooleanField(default=False)

class Reader(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    bio = models.TextField()
    profile_picture = models.IntegerField(default=0) # mengacu ke tipe profile picturenya. buat tugas ini 0 = default.
    preferences = models.OneToOneField(ReaderPreferences)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    reviews = models.OneToOneField(Review, on_delete=models.CASCADE)