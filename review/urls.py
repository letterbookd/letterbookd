from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('', show_reviews, name='show_reviews'),
    path('my-reviews/', get_all_user_reviews, name='my_reviews'),
    path('review/<int:id>', get_user_review, name='get_review'),
    path('new/<int:id>', create_review, name='create_review'),
    path('edit/<int:id>', edit_review, name='edit_review'),
    path('delete/<int:id>', delete_review, name='deletet_review'),
]
