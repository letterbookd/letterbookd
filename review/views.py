from django.shortcuts import render

from review.models import Review
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse

# Create your views here.
def show_reviews(request, book_id):
    # TODO: render semua review dari buku
    return

def get_all_user_reviews(request):
    # TODO: mengembalikan json isinya semua review milik Reader
    return

def get_user_review(request, book_id):
    # TODO: mengembalikan json review Reader untuk suatu buku
    return

def create_review(request, book_id):
    # TODO: bikin review baru (ajax)
    return

def edit_review(request, review_id):
    # TODO: edit reviewnya (ajax)
    return

def delete_review(request, review_id):
    # TODO: hapus reviewnya (ajax)
    return  