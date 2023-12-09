from django.shortcuts import render

from catalog.models import *
from review.models import *
from library.models import *
from reader.models import *
from catalog.forms import BookForm
from django.forms import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json

def book_in_library(request, id):
    reader = Reader.objects.get(user=request.user)
    library = reader.personal_library
    book = Book.objects.get(pk=id)

    target_book = LibraryBook.objects.filter(library=library, book=book)
    return HttpResponse(serializers.serialize('json', target_book))


@login_required(login_url='/login')
def show_librarian_catalog(request):
    get_object_or_404(Librarian, user=request.user) #authorize librarian

    books = Book.objects.all()
    
    #add django form
    form = BookForm()

    context = {
        'books': books,
        'form': form,
        'page_title':'Librarian Catalog',
    }
    return render(request, "librarian_catalog.html", context)

def get_related_books(request):
    library_items = get_object_or_404(Library, reader__user=request.user).mybooks.all()
    book_items = Book.objects.filter(librarybook__in=library_items)

    return HttpResponse(serializers.serialize('json', book_items))

def get_related_books_json(request):
    library_items = get_object_or_404(Library, reader__user=request.user).mybooks.all()
    book_items = Book.objects.filter(librarybook__in=library_items)

    library = []
    for book in book_items:
        library.append({"model": 'catalog.book', 
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
                                    "favorites_count": book.favorites_count}
                                })

    return JsonResponse({'library':library})

def get_username(request):
    username = request.user.username
    return JsonResponse({'username':username})

#====================================================================================
@login_required(login_url='/login')
def show_reader_catalog(request):
    get_object_or_404(Reader, user=request.user) #authorize  reader

    books = Book.objects.all()

    context = {
        'books': books,
        'page_title':'Catalog',
    }
    return render(request, "reader_catalog.html", context)

@login_required(login_url='/login')
def show_book_detail(request,id):
    get_object_or_404(Reader, user=request.user) #authorize  reader
    
    book = Book.objects.get(pk=id)

    context = {
        'book': book,
        'authors': book.authors.replace(";", ", "),
        'page_title': book.title + " - Catalog",
    }

    return render(request, "book_detail.html", context)

def get_book_json(request):
    book = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book))

def get_favorited_library_book(request, id):
    book = Book.objects.get(pk=id)

    target_books = LibraryBook.objects.filter(book=book, is_favorited=True)
    return HttpResponse(serializers.serialize('json', target_books))

@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        isbn13 = request.POST.get("isbn13")
        title = request.POST.get("title")
        authors = request.POST.get("authors")
        categories = request.POST.get("categories")
        thumbnail = request.POST.get("thumbnail")
        description = request.POST.get("description")
        published_year = request.POST.get("published_year")
        page_count = request.POST.get("page_count")

        new_book = Book(isbn13=isbn13, title=title, authors=authors, categories=categories, thumbnail=thumbnail, description=description, published_year=published_year, page_count=page_count)
        new_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def edit_book_ajax(request, id):
    if request.method == 'POST':
        isbn13 = request.POST.get("isbn13")
        title = request.POST.get("title")
        authors = request.POST.get("authors")
        categories = request.POST.get("categories")
        thumbnail = request.POST.get("thumbnail")
        description = request.POST.get("description")
        published_year = request.POST.get("published_year")
        page_count = request.POST.get("page_count")

        book = Book.objects.get(pk = id)

        book.isbn13 = isbn13
        book.title = title
        book.authors = authors
        book.categories = categories
        book.thumbnail = thumbnail
        book.description = description
        book.published_year = published_year
        book.page_count = page_count
        book.overall_rating = book.overall_rating
        book.favorites_count = book.favorites_count
        book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_book_ajax(request, id):
    if request.method == 'DELETE':
        Book.objects.get(pk=id).delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_book_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_book = Book.objects.create(
            isbn13 = int(data["isbn13"]),
            title = data["title"],
            authors = data["authors"],
            categories = data["categories"],
            thumbnail = data["thumbnail"],
            description = data["description"],
            published_year = int(data["publised_year"]),
            page_count = int(data["page_count"]),
            overall_rating = 0.0,
            favorites_count = 0,
        )

        new_book.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_book_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        
        id = int(data["pk"])

        book = Book.objects.get(pk = id)

        book.isbn13 = int(data["isbn13"])
        book.title = data["title"]
        book.authors = data["authors"]
        book.categories = data["categories"]
        book.thumbnail = data["thumbnail"]
        book.description = data["description"]
        book.published_year = int(data["publised_year"])
        book.page_count = int(data["page_count"])
        book.overall_rating = 0.0
        book.favorites_count = 0

        book.save()

        book_data = [{"model": 'catalog.book', 
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
                                "favorites_count": book.favorites_count}
                            }]

        return JsonResponse({"status": "success", "book_data": book_data}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_book_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = int(data["id"])

        Book.objects.get(pk=id).delete()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)