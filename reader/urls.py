from django.urls import path
from reader.views import *

app_name = 'reader'

urlpatterns = [
    path('<int:id>/', show_profile, name='show_profile'),
    path('search/<str:name>', search_reader, name='search_reader'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('get-reader/', get_all_readers_json, name='get_all_readers_json'),
    path('edit-profile-ajax/<int:id>/', edit_profile_ajax, name='edit_profile_ajax'),
    path('search/', search_handler, name='search_handler'),
]