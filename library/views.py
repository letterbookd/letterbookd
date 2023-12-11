import json
from django.shortcuts import render, get_object_or_404

from reader.models import Reader
from library.models import Library, LibraryBook
from library.forms import LibraryBookForm, UpdateLibBookForm
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
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
def api_get_library(request):
    ''' Mengembalikan JSON data library milik user '''
    library_items = get_object_or_404(Library, reader__user=request.user).mybooks.all()
    book_items = Book.objects.filter(librarybook__in=library_items)

    library = [
        [{
            "model": 'library.librarybook',
            "pk": libbook.pk,
            "fields": {"library": libbook.library.pk,
                       "book": libbook.book.pk,
                       "tracking_status": libbook.tracking_status,
                       "is_favorited": libbook.is_favorited,
                       "is_reviewed": libbook.is_reviewed
                       }
        } for libbook in library_items],
        [{
            "model": 'catalog.book',
            "pk": book.pk,
            "fields": {"isbn13": book.isbn13,
                       "title": book.title,
                       "authors": book.authors,
                       "categories": book.categories,
                       "thumbnail": book.thumbnail,
                       "description": book.description,
                       "published_year": book.published_year,
                       "page_count": book.page_count,
                       "overall_rating": book.overall_rating,
                       "favorites_count": book.favorites_count,
                       }
        } for book in book_items],
    ]
    return JsonResponse({"library": library}, safe=False)

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
@csrf_exempt
def api_update_book_status(request, id):
    ''' Mengupdate status tracking buku yang ada di library '''

    reader_library = get_object_or_404(Library, reader__user=request.user)
    library_book = get_object_or_404(LibraryBook, book__id=id, library=reader_library)
    isFavorited = bool(request.POST.get('isFavorited', library_book.is_favorited))
    trackingStatus = int(request.POST.get('trackingStatus', library_book.tracking_status))

    if library_book:
        library_book.is_favorited = isFavorited
        library_book.tracking_status = trackingStatus
        library_book.save()
        return JsonResponse({"status": True, "message": "Updated!"}, status=201)
    
    return JsonResponse({"status": False, "message": "Cannot find book in library"}, status=400)

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
@csrf_exempt
def api_add_book(request):
    return

@login_required(login_url='/login')
@require_POST
def remove_book(request, id):
    ''' Mengeluarkan buku dari library milik user '''
    
    reader_library = get_object_or_404(Library, reader__user=request.user)
    book_to_delete = get_object_or_404(LibraryBook, book__id=id, library=reader_library)
    book_to_delete.delete()
    
    return HttpResponse(b"DELETED", status=201)

@login_required(login_url='/login')
@require_POST
@csrf_exempt
def api_remove_book(request, id):
    return