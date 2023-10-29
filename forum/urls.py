from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', thread_list, name='forum'),
    path('create/', create_thread, name='create_thread'),
    path('view/<int:thread_id>/', view_thread, name='view_thread'),
    path('reply/<int:thread_id>/', reply_to_thread, name='reply_to_thread'),
    path('edit/<int:thread_id>/', edit_thread, name='edit_thread'),
    path('delete/<int:thread_id>/', delete_thread, name='delete_thread'),
    path('like/<int:thread_id>/', like_thread, name='like_thread'),
    path('user_thread', user_thread_data, name='user_thread'),
    path('user_liked_thread', user_liked_thread_data, name='user_liked_thread'),
]