from django.db import models
from django.contrib.auth.models import User

# TODO
class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField()
    replying_to = models.OneToOneField(to="ForumPost", null=True)

class ForumThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField()
    tags = models.CharField() # separated by semicolon
    date_started = models.DateTimeField(auto_now_add=True)
    initial_post = models.OneToOneField(ForumPost, on_delete=models.CASCADE)