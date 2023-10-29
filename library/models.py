from django.db import models
from reader.models import *
from catalog.models import *

# Create your models here.
class Library(models.Model):
    def __str__(self):
        return f"{self.reader.display_name}'s library"
    pass

class LibraryBook(models.Model):
    ''' Data untuk buku yang ada di Library '''

    TRACKING_STATUS = [
        (1, "Finished Reading"),
        (2, "Currently Reading"),
        (3, "On Hold"),
        (4, "Planning to Read"),
        (5, "Dropped"),
    ]

    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='mybooks')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False)
    tracking_status = models.IntegerField(default=0, choices=TRACKING_STATUS, blank=False) # 0: UNTRACKED, 1: FINISHED, 2: READING, 3: ON HOLD, 4: PLANNED, 5: DROPPED
    is_favorited = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"\"{self.book.title}\" in {self.library.reader.display_name}'s library"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['library', 'book'], name='lib_book_link')
        ]