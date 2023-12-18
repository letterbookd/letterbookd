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
    path('search-readers/', search_readers_api, name='search_readers_api'),
    path('get-reader-json/', get_reader_json, name='get_reader_json'),
    path('get-readers-json/', get_readers_json, name='get_readers_json'),
    path('update-profile/', update_profile, name='update_profile'),
    
    # ======
    path('reader-library-api/<str:username>/', reader_library_api, name='reader_library_api'),
    path('reader-review-api/<str:username>/', reader_review_api, name='reader_review_api'),

]