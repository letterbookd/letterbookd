from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'threads'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(Thread, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"\"{self.title}\" THREAD by {self.created_by.username}"


class Like(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'

    def __str__(self) -> str:
        return f"\"{self.thread.title}\" LIKE by {self.created_by.username}"


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'replies'

    def __str__(self) -> str:
        return f"REPLY by {self.created_by.username} to \"{self.thread.title}\""
