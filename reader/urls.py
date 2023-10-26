from django.urls import path
from reader.views import *

app_name = 'reader'

urlpatterns = [
    path('<int:id>/', show_profile, name='show_profile'),
    path('search/<str:name>', search_reader, name='search_reader'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('settings/', user_settings, name='user_settings'),
    path('apply-settings/', apply_settings, name='apply_settings'),
]