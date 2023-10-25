from django.shortcuts import render

from catalog.models import Book
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#nanti authenticate
def show_books(request):
    books = Book.objects.all()

    context = {
        'books': books,
    }
    return render(request, "librarian_catalog.html", context)

def get_book_json(request):
    book = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book))

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

def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
