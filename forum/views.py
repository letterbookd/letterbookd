from django.shortcuts import render

from forum.models import ForumPost, ForumThread
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse

def show_threads(request):
    # TODO: render halaman utama yg isinya semua forumthread yang ada
    return

def get_threads(request, filter):
    # TODO: mengembalikan json isinya ForumThread sesuai filter
    return

def create_thread(request):
    # TODO: membuat thread baru (ajax)
    return

def edit_thread(request, id):
    # TODO: mengedit thread milik Reader tersebut (ajax)
    return

def delete_thread(request, id):
    # TODO: menghapus thread milik Reader tersebut (ajax)
    return

def post_reply(request, post_id):
    # TODO: baut ForumPost (reply) baru ke ForumPost dengan post_id (ajax)
    return

def edit_reply(request, id):
    # TODO: mengedit reply milik Reader tersebut (ajax)
    return

def delete_reply(request, id):
    # TODO: menghapus reply milik Reader tersebut (ajax)
    return