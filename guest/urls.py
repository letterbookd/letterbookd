from django.urls import path
from guest.views import *

app_name = 'guest'

urlpatterns = [
    path('', show_landing, name='landing_page'),
]