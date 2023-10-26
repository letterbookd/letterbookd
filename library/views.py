from django.shortcuts import render, get_object_or_404

from reader.models import Reader
from library.models import Library
from catalog.models import Book
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse

# Create your views here.
def show_library(request):
    # TODO render halaman library
    context = {'page_title': "Library", 'display_name': get_object_or_404(Reader, user=request.user).display_name}
    return render(request, './library.html', context)

def get_library(request):
    # TODO mengembalikan json data library user
    return

def filter_library(request, arg):
    # TODO filter library sesuai arg
    return

def sort_library(request, arg):
    # TODO mengembalikan json data library user yang sudah di sort
    return

def add_book(request, book_id):
    # TODO nambah buku
    return

def remove_book(request, book_id):
    # TODO ilangin buku
    return

def favorite_book(request, book_id):
    # TODO add ke library (kalau belum) dan favorite bukunya
    return 