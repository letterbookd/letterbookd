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

@login_required(login_url='/login')
def show_librarian_catalog(request):
    get_object_or_404(Librarian, user=request.user) #authenticate librarian

    books = Book.objects.all()
    
    #handle django form
    form = BookForm()

    if(request.method == "POST"):
        form = BookForm(request.POST or None)

        if form.is_valid() and request.method == "POST":
            book = form.save(commit=False)
            book.save()
            return JsonResponse(model_to_dict(book, fields=["isbn13", "title", "authors", "categories", "thumbnail", "description", "published_year", "page_count", "overall_rating", "favorites_count"]), status=201)

    context = {
        'books': books,
        'form': form,
        'page_title':'LibrarianCatalog',
    }
    return render(request, "librarian_catalog.html", context)

#====================================================================================
@login_required(login_url='/login')
def show_reader_catalog(request):
    get_object_or_404(Reader, user=request.user) #authenticate reader

    books = Book.objects.all()

    context = {
        'books': books,
        'page_title':'ReaderCatalog',
    }
    return render(request, "reader_catalog.html", context)

@login_required(login_url='/login')
def show_book_detail(request,id):
    get_object_or_404(Reader, user=request.user) #authenticate reader
    
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
