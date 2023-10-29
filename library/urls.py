from django.urls import path
from library.views import *

app_name = 'library'

urlpatterns = [
    path('', show_library, name='show_library'),
    path('get/', get_library, name='get_library'),
    path('add/', add_book, name='add_book'),
    path('remove/', remove_book, name='remove_book'),
    path('fav/', favorite_book, name='favorite_book'),
]