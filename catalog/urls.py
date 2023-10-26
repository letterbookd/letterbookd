from django.urls import path
from catalog.views import get_book_json, add_book_ajax, show_librarian_catalog, show_reader_catalog, show_book_detail,show_json, show_json_by_id, edit_book_ajax, delete_book_ajax

app_name = 'catalog'

urlpatterns = [
    path('librarian-catalog/', show_librarian_catalog, name='show_librarian_catalog'),
    path('reader-catalog/', show_reader_catalog, name='show_reader_catalog'),
    path('book-detail/<int:id>', show_book_detail, name='show_book_detail'),
    path('add-book/', add_book_ajax, name='add_book_ajax'),
    path('get-book/', get_book_json, name='get_book_json'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-book/<int:id>/', edit_book_ajax, name='edit_book_ajax'),
    path('delete-book/<int:id>/', delete_book_ajax, name='delete_book_ajax'),
]