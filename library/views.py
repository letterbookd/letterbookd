from django.shortcuts import render, get_object_or_404

from reader.models import Reader
from library.models import Library, LibraryBook
from library.forms import LibraryBookForm
from django.db import IntegrityError
from catalog.models import Book
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
    return JsonResponse({"library" : library})

@login_required(login_url='/login')
@require_POST
def update_book_status(request, book_id, status_code):
    ''' Mengupdate status tracking buku yang ada di library '''
    book_to_update = Book.objects.get(pk=book_id)
    if (book_to_update is None):
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_update)
    if lib_book is not None:
        return HttpResponseNotFound()
    
    lib_book.tracking_status = status_code
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
            book_to_add.library = get_object_or_404(Library, reader__user=request.user)
            book_to_add.save()
            bookForm.save_m2m()
            return HttpResponse(b"CREATED", status=201)
        
    return HttpResponse(b"EXISTS", status=409)

@login_required(login_url='/login')
@require_POST
def remove_book(request):
    ''' Mengeluarkan buku dari library milik user '''
    book_to_remove = Book.objects.get()
    if book_to_remove is None:
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_remove)
    if lib_book is None:
        return HttpResponseNotFound()
    
    lib_book.delete()
    return HttpResponse(b"DELETED", status=201)

@login_required(login_url='/login')
@require_POST
def favorite_book(request):
    ''' Menandakan buku  sebagai favorit (dan sebaliknya) '''
    book_to_fav = Book.objects.get()
    if book_to_fav is None:
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_fav)
    if lib_book is None:
        lib_book = LibraryBook()
        lib_book.library = get_object_or_404(Library, reader__user=request.user)
        lib_book.book = book_to_fav
        lib_book.tracking_status = 0 # default: untracked
        lib_book.is_favorited = True
        lib_book.save()
        return HttpResponseNotFound()
    
    lib_book.is_favorited = not lib_book.is_favorited
    return HttpResponse(b"FAVORITED", status=201)