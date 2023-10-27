from django.shortcuts import render

from catalog.models import *
from review.models import *
from library.models import *
from reader.models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

#temporary functions =========================================================================================================
@csrf_exempt
def add_review(request, id):
    if request.method == 'POST':
        book = Book.objects.get(pk=id)

        reader = Reader.objects.get(user=request.user)
        
        new_review = Review(user=reader, book=book, stars_rating=4, status_on_review="ON HOLD", review_text="blablabla")
        new_review.save()

        reviews = Review.objects.filter(book=book)
        total_rating = 0
        total_reviews = len(reviews)

        for review in reviews:
            total_rating += review.stars_rating
        
        book.overall_rating = round((total_rating / total_reviews), 2)
        book.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_review(request, id):
    if request.method == 'DELETE':
        book = Book.objects.get(pk=id)
        reviews = Review.objects.filter(book=book)
        book.overall_rating = 0
        book.save()
        reviews.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

def get_reviews_json(request, id):
    book = Book.objects.get(pk=id)
    reviews = Review.objects.filter(book=book)
    return HttpResponse(serializers.serialize('json', reviews))

def show_book_reviews(request, id):
    book = Book.objects.get(pk=id)
    reviews = Review.objects.filter(book=book)

    context = {
        'book': book,
        'reviews': reviews,
        'page_title':'BookReviews',
    }

    return render(request, "book_reviews.html", context)

#untuk handle button favorite
def get_book_in_user_library(request, id):
    reader = Reader.objects.get(user=request.user)
    reader_library = reader.personal_library
    book = Book.objects.get(pk=id)

    target_book = LibraryBook.objects.filter(library=reader_library, book=book)

    return HttpResponse(serializers.serialize('json', target_book))

def get_favorited_books(request):
    reader = Reader.objects.get(user=request.user)
    reader_library = reader.personal_library

    target_fav_books = LibraryBook.objects.filter(library=reader_library, is_favorited=True)
    return HttpResponse(serializers.serialize('json', target_fav_books))

@csrf_exempt
def add_to_favorite(request, id):
    if request.method == 'POST':
        book = Book.objects.get(pk=id)
        reader = Reader.objects.get(user=request.user)
        reader_library = reader.personal_library

        new_library_book = LibraryBook(library=reader_library, book=book, tracking_status=0, is_favorited=True)
        new_library_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_favorites(request):
    if request.method == 'DELETE':
        reader = Reader.objects.get(user=request.user)
        library = reader.personal_library

        library_books = LibraryBook.objects.filter(library=library)
        library_books.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

#================================================================================================================

#nanti authenticate
def show_librarian_catalog(request):
    books = Book.objects.all()

    context = {
        'books': books,
        'page_title':'LibrarianCatalog',
    }
    return render(request, "librarian_catalog.html", context)

def show_reader_catalog(request):
    books = Book.objects.all()

    context = {
        'books': books,
        'page_title':'ReaderCatalog',
    }
    return render(request, "reader_catalog.html", context)

def show_book_detail(request,id):
    book = Book.objects.get(pk=id)

    context = {
        'book': book,
        'authors': book.authors.replace(";", ", "),
        'page_title':'BookDetail',
    }

    return render(request, "book_detail.html", context)

def get_book_json(request):
    book = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book))

def get_favorited_library_book(request, id):
    book = Book.objects.get(pk=id)

    target_books = LibraryBook.objects.filter(book=book)
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
