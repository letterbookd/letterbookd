from django.shortcuts import render, get_object_or_404

from reader.models import Reader
from library.models import Library, LibraryBook
from catalog.models import Book
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET

# Create your views here.
@login_required(login_url='/login')
def show_library(request):
    library = get_object_or_404(Library, reader__user=request.user).mybooks.all()

    context = {
        'page_title': "Library",
        'display_name': get_object_or_404(Reader, user=request.user).display_name,
        'library': library,
    }
    return render(request, './library.html', context)

@login_required(login_url='/login')
def get_library(request):
    # TODO mengembalikan json data library user
    library_items = get_object_or_404(Library, reader__user=request.user).mybooks.all()
    return HttpResponse(serializers.serialize('json', library_items))

@login_required(login_url='/login')
def get_book_in_library(request, book_id):
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book__pk=book_id)
    return HttpResponse(serializers.serialize('json', lib_book))

@login_required(login_url='/login')
@require_POST
def update_book_status(request, book_id, status_code):
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
def add_book(request, book_id):
    book_to_add = Book.objects.get(pk=book_id)
    if (book_to_add is None):
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_add)
    if lib_book is not None:
        return HttpResponseNotFound()
    
    lib_book = LibraryBook()
    lib_book.library = get_object_or_404(Library, reader__user=request.user)
    lib_book.book = book_to_add
    lib_book.tracking_status = 0
    lib_book.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login')
@require_POST
def remove_book(request, book_id):
    book_to_remove = Book.objects.get(pk=book_id)
    if book_to_remove is None:
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_remove)
    if lib_book is None:
        return HttpResponseNotFound()
    
    lib_book.delete()
    return HttpResponse(b"DELETED", status=201)

@login_required(login_url='/login')
@require_POST
def favorite_book(request, book_id):
    book_to_fav = Book.objects.get(pk=book_id)
    if book_to_fav is None:
        return HttpResponseNotFound()
    
    lib_book = get_object_or_404(Library, reader__user=request.user).mybooks.get(book=book_to_fav)
    if lib_book is None:
        lib_book = LibraryBook()
        lib_book.library = get_object_or_404(Library, reader__user=request.user)
        lib_book.book = book_to_fav
        lib_book.tracking_status = 0
        lib_book.is_favorited = True
        lib_book.save()
        return HttpResponseNotFound()
    
    lib_book.is_favorited = not lib_book.is_favorited
    return HttpResponse(b"FAVORITED", status=201)