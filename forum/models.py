from django.db import models
from reader.models import *

# TODO
class ForumPost(models.Model):
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    message_text = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField()
    replying_to = models.OneToOneField(to="ForumPost", null=True, on_delete=models.CASCADE)

class ForumThread(models.Model):
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255) # separated by semicolon
    date_started = models.DateTimeField(auto_now_add=True)
    initial_post = models.OneToOneField(ForumPost, on_delete=models.CASCADE)