from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django import forms
from django.contrib.auth.models import UserManager



# Create your models here.
class GuestModel(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'guest'

    def authenticate(self, request, username=None, password=None):
        try:
            user = self.objects.get(username=username, password=password)
            if user.check_password(password):
                return user
            return None
        except self.DoesNotExist:
            return None
        
    def get_profile(self):
        return self

    def __str__(self):
        return self.username