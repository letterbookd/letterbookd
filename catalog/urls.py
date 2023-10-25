from django.urls import path
from catalog.views import get_book_json, add_book_ajax, show_books, show_json, show_json_by_id, show_xml, show_xml_by_id, edit_book_ajax, delete_book_ajax

app_name = 'catalog'

urlpatterns = [
    path('', show_books, name='show_books'),
    path('add-book/', add_book_ajax, name='add_book_ajax'),
    path('get-book/', get_book_json, name='get_book_json'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('edit-book/<int:id>/', edit_book_ajax, name='edit_book_ajax'),
    path('delete-book/<int:id>/', delete_book_ajax, name='delete_book_ajax'),
]