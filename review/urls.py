from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('', show_all_reviews, name='show_all_reviews'),
    path('show-reviews/<int:book_id>', show_reviews, name='show_reviews'),

    path('my-reviews/', get_all_user_reviews, name='my_reviews'),
    # path('review/<int:id>', get_user_review, name='get_review'),

    path('book-in-library/<int:book_id>', book_in_library, name='book_in_library'),

    path('new-ajax/<int:book_id>', create_review_ajax, name='create_review_ajax'),
    path('edit/<int:id>', edit_review, name='edit_review'),
    path('delete/<int:id>', delete_review, name='delete_review'),

    path('json/', show_json, name='show_json'), 
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),

]