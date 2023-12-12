from django.db import models
from django.contrib.auth.models import User
from library.models import *
from catalog.models import *

class ReaderPreferences(models.Model):
    share_reviews = models.BooleanField(default=True)
    share_library = models.BooleanField(default=False)

    def __str__(self):
        return self.reader.display_name + "'s Reader preferences"

class Reader(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, null=True)
    bio = models.TextField(null=True, blank=True, default="")
    profile_picture = models.IntegerField(default=0)
    personal_library = models.OneToOneField(Library, on_delete=models.CASCADE, null=True)
    preferences = models.OneToOneField(ReaderPreferences, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.display_name + "'s Reader account"