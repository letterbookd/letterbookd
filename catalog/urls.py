from django.urls import path
from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('', show_reader_catalog, name='show_reader_catalog'),
    path('librarian-catalog/', show_librarian_catalog, name='show_librarian_catalog'),
    path('book-detail/<int:id>', show_book_detail, name='show_book_detail'),
    path('add-book/', add_book_ajax, name='add_book_ajax'),
    path('get-book/', get_book_json, name='get_book_json'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-book/<int:id>/', edit_book_ajax, name='edit_book_ajax'),
    path('delete-book/<int:id>/', delete_book_ajax, name='delete_book_ajax'),
    path('get-favorited-library-book/<int:id>', get_favorited_library_book, name='get_favorited_library_book'),

    #temporary urls ==============================================================================================
    path('reviews/<int:id>/', show_book_reviews, name='show_book_reviews'),
    path('get-reviews/<int:id>/', get_reviews_json, name='get_reviews_json'),
    path('add-review/<int:id>/', add_review, name='add_review'),
    path('delete-review/<int:id>/', delete_review, name='delete_review'),

    path('get-book-from-user-library/<int:id>/', get_book_in_user_library, name='get_book_in_user_library'),
    path('get-favorited-books/', get_favorited_books, name='get_favorited_books'),
    path('add-to-favorite/<int:id>', add_to_favorite, name='add_to_favorite'),
    path('delete-favorites/', delete_favorites, name='delete_favorites'),
]