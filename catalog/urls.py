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
    path('get-related-books/', get_related_books, name='get_related_books'),

    path('get-username/', get_username, name='get_username'),
    path('get-related-books-json/', get_related_books_json, name='get_related_books_json'),
]