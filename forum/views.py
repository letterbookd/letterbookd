from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from forum.models import Thread, Reply, Like
from forum.forms import ThreadForm, RepliesForm, DivErrorList
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='/login')
def thread_list(request):
    threads = Thread.objects.annotate(likes=Count('like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    return render(request, 'forum.html', {'threads': threads})


@login_required(login_url='/login')
def user_thread_data(request):
    user = request.user
    threads = Thread.objects.filter(created_by=user).annotate(likes=Count('like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    return threads


@login_required(login_url='/login')
def user_liked_thread_data(request):
    user = request.user
    liked_threads = Thread.objects.filter(like__created_by=user).annotate(likes=Count('like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    return liked_threads


@login_required(login_url='/login')
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