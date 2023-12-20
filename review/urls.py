from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('', show_all_reviews, name='show_all_reviews'),
    path('show-reviews/<int:book_id>', show_reviews, name='show_reviews'),
    path('my-reviews/', get_all_user_reviews, name='my_reviews'),
    path('book-in-library/<int:book_id>', book_in_library, name='book_in_library'),
    path('new-ajax/<int:book_id>', create_review_ajax, name='create_review_ajax'),
    path('edit/<int:id>', edit_review, name='edit_review'),
    path('delete/<int:id>', delete_review, name='delete_review'),
    path('json/', show_json, name='show_json'), 
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    #-------------------------------Flutter Function-----------------------------------#
    path('show_review_flutter/', show_review_flutter, name='show_review_flutter'),
    path('show_review_flutter_by_user/', show_review_flutter_by_user, name='show_review_flutter_by_user'),
    path('show_review_by_book_flutter/<int:id_buku>/', show_review_by_book_flutter, name='show_review_by_book_flutter'),
    path('get_username_by_id/<int:user_id>/', get_username_by_id, name='get_username_by_id'),
    path('get_book_title_by_id/<int:id_buku>/', get_book_title_by_id, name='get_book_title_by_id'),
    path('create_review_flutter/', create_review_flutter, name='create_review_flutter'),
    path('delete_review_flutter/', delete_review_flutter, name='delete_review_flutter'),
    path('update_review_flutter/', update_review_flutter, name='update_review_flutter'),
]