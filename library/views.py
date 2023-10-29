from django.shortcuts import render, get_object_or_404

from reader.models import Reader
from library.models import Library, LibraryBook
from library.forms import LibraryBookForm, UpdateLibBookForm
from django.db import IntegrityError
from catalog.models import Book
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET

# Create your views here.
@login_required(login_url='/login')
def show_library(request):
    ''' Menampilkan library milik user '''
   
    lib_book = get_object_or_404(Library, reader__user=request.user)
    context = {
        'page_title': "Library",
        'display_name': get_object_or_404(Reader, user=request.user).display_name,
        'form': LibraryBookForm(instance=LibraryBook(library=lib_book))
    }
    return render(request, './library.html', context)

@login_required(login_url='/login')
def get_library(request):
    ''' Mengembalikan JSON data library milik user '''
    library_items = get_object_or_404(Library, reader__user=request.user).mybooks.all()
    book_items = Book.objects.filter(librarybook__in=library_items)

    library_items = list(library_items.values())
    book_items = list(book_items.values())
    library = []
    for index in range(0, len(library_items)):
        library.append(
            {
                "library_data": library_items[index],
                "book_data": book_items[index],
            }
        )
    return JsonResponse({"library": library})

@login_required(login_url='/login')
def get_lib_book_form(request, id):
    ''' Mengembalikan ModelForm untuk LibraryBook'''

    reader_library = get_object_or_404(Library, reader__user=request.user)
    bookForm = UpdateLibBookForm(instance=get_object_or_404(LibraryBook, book__id=id, library=reader_library))
    return HttpResponse(bookForm.as_div())

@login_required(login_url='/login')
@require_POST
def update_book_status(request, id):
    ''' Mengupdate status tracking buku yang ada di library '''

    reader_library = get_object_or_404(Library, reader__user=request.user)
    bookForm = UpdateLibBookForm(request.POST, instance=get_object_or_404(LibraryBook, book__id=id, library=reader_library))
    if bookForm.is_valid():
        bookForm.save()
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponse(b"UPDATED", status=201)

@login_required(login_url='/login')
@require_POST
def add_book(request):
    ''' Menambah buku kedalam library milik user '''

    reader_library = get_object_or_404(Library, reader__user=request.user)
    bookForm = LibraryBookForm(request.POST)
    if bookForm.is_valid():
        book_to_add = bookForm.save(commit=False)
        try:
            LibraryBook.objects.get(library=reader_library, book=book_to_add.book)
        except LibraryBook.DoesNotExist:
            book_to_add.library = reader_library
            book_to_add.save()
            bookForm.save_m2m()
            return HttpResponse(b"CREATED", status=201)
        
    return HttpResponse(b"EXISTS", status=409)

@login_required(login_url='/login')
@require_POST
def remove_book(request, id):
    ''' Mengeluarkan buku dari library milik user '''
    
    reader_library = get_object_or_404(Library, reader__user=request.user)
    book_to_delete = get_object_or_404(LibraryBook, book__id=id, library=reader_library)
    book_to_delete.delete()
    
    return HttpResponse(b"DELETED", status=201)