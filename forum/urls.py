from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', thread_list, name='forum'),
    path('json/', thread_list_json, name='forum-json'),
    path('create/', create_thread, name='create_thread'),
    path('create-json/', create_thread_json, name='create_thread_json'),
    path('view/<int:thread_id>/', view_thread, name='view_thread'),
    path('view-json/<int:thread_id>/', view_thread_json, name='view_thread_json'),

    path('reply/<int:thread_id>/', reply_to_thread, name='reply_to_thread'),
    path('reply-json/<int:thread_id>/', reply_to_thread_json,
         name=' reply_to_thread_json'),
    path('edit/<int:thread_id>/', edit_thread, name='edit_thread'),
    path('edit-json/<int:thread_id>/', edit_thread_json, name='edit_thread_json'),
    path('delete/<int:thread_id>/', delete_thread, name='delete_thread'),
    path('delete-json/<int:thread_id>/',
         delete_thread_json, name='delete_thread_json'),

    path('like/<int:thread_id>/', like_thread, name='like_thread'),
    path('like-json/<int:thread_id>/', like_thread_json, name='like_thread_json'),
    path('user_thread', user_thread_data, name='user_thread'),
    path('user_liked_thread', user_liked_thread_data, name='user_liked_thread'),
]
