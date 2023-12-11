from django.urls import path
from library.views import *

app_name = 'library'

urlpatterns = [
    path('', show_library, name='show_library'),
    path('get/', get_library, name='get_library'),
    path('add/', add_book, name='add_book'),
    path('update/<int:id>', update_book_status, name='update_status'),
    path('remove/<int:id>', remove_book, name='remove_book'),

    # flutter apis
    path('api/get/', api_get_library, name='api_get_library'),
    path('api/add/', api_add_book, name='api_add_book'),
    path('api/update/<int:id>', api_update_book_status, name='api_update_book_status'),
    path('api/remove/<int:id>', api_remove_book, name='api_remove_book'),
]