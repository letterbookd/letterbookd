from django.shortcuts import render

from reader.models import Reader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse

# Create your views here.
def show_profile(request, id):
    # TODO: render halaman profil Reader dengan id
    return

def search_reader(request, display_name):
    # TODO: mengembalikan halaman hasil searching Reader dengan display_name (__icontains)
    return

def edit_profile(request):
    # TODO: mengedit profil (display_name dan bio) user dari halaman profilenya (AJAX)
    return

def user_settings(request):
    # TODO: render halaman setting untuk Reader
    return

def apply_settings(request):
    # TODO: mengapply setting untuk Reader (AJAX)
    return