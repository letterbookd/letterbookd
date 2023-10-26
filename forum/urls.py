from django.urls import path
from forum.views import *

app_name = 'forum'

urlpatterns = [
    path('', show_threads, name='show_threads'),
    path('thread/<int:id>/', get_threads, name='get_thread'),
    path('new/', create_thread, name='create_threads'),
    path('edit/<int:id>', edit_thread, name='edit_thread'),
    path('delete/<int:id>', delete_thread, name='delete_thread'),
    path('reply/<int:id>', post_reply, name='post_reply'),
    path('edit_reply/<int:id>', edit_reply, name='edit_reply'),
    path('delete_reply/<int:id>', delete_reply, name='delete_reply'),

]