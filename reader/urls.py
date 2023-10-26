from django.urls import path
from reader.views import *

app_name = 'reader'

urlpatterns = [
    path('<int:id>/', show_profile, name='show_profile'),
    path('search/<str:name>', search_reader, name='search_reader'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('settings/', user_settings, name='user_settings'),
    path('apply-settings/', apply_settings, name='apply_settings'),
    path('search-catalog/', search_catalog, name='search_catalog'), 
    path('search-library/', search_library, name='search_library'), 
    path('get-reader-data/<int:user_id>/', get_reader_data_by_user, name='get_reader_data_by_user'), 
    path('update-reader-settings-ajax/', update_reader_settings_ajax, name='update_reader_settings_ajax'),
]
