from django.db import models
from reader.models import *
from catalog.models import *

# Create your models here.
class Library(models.Model):
    pass

class LibraryBook(models.Model):
    ''' Data untuk buku yang ada di Library '''
    
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tracking_status = models.IntegerField() # 0: UNTRACKED, 1: FINISHED, 2: READING, 3: ON HOLD, 4: PLANNED, 5: DROPPED
    is_favorited = models.BooleanField(default=False)