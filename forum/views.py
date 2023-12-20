from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from forum.models import Thread, Reply, Like
from forum.forms import ThreadForm, RepliesForm, DivErrorList
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user

import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user


# Create your views here.


@login_required(login_url='/login')
def thread_list(request):
    threads = Thread.objects.annotate(likes=Count('like', distinct=True)).annotate(
        rep=Count('replies')).order_by('-created_at')

    return render(request, 'forum.html', {'page_title': 'Forum', 'threads': threads})


def thread_list_json(request):
    threads = Thread.objects.all().order_by('-created_at')
    threads_with_like_count = Thread.objects.annotate(like_count=Count('like'))

# Mengurutkan thread berdasarkan jumlah like secara descending
    sorted_threads = threads_with_like_count.order_by('-like_count')
    # Convert QuerySet to JSON

    threads_json = [{"model": 'thread.model', "pk": thread.pk, "fields": {"title": remove_parentheses(thread.title), "content": remove_parentheses(thread.content),
                                                                          "created_by": thread.created_by.username, "created_at": thread.created_at, "updated_at": thread.updated_at}} for thread in threads if thread.created_by is not None]

    threads_by_like_json = [{"model": 'thread.model', "pk": thread.pk, "fields": {"title": remove_parentheses(thread.title), "content": remove_parentheses(thread.content),
                                                                                  "created_by": thread.created_by.username, "created_at": thread.created_at, "updated_at": thread.updated_at}} for thread in sorted_threads if thread.created_by is not None]

    # You can also use JsonResponse to return a JSON response
    return JsonResponse({'page_title': 'Forum', 'threads': threads_json, 'threads_by_like': threads_by_like_json}, safe=False)


@login_required(login_url='/login')
def user_thread_data(request):
    user = request.user
    threads = Thread.objects.filter(created_by=user).annotate(likes=Count(
        'like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    threads = Thread.objects.filter(created_by=user).annotate(likes=Count(
        'like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    return threads


@login_required(login_url='/login')
def user_liked_thread_data(request):
    user = request.user
    liked_threads = Thread.objects.filter(like__created_by=user).annotate(likes=Count(
        'like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    liked_threads = Thread.objects.filter(like__created_by=user).annotate(likes=Count(
        'like', distinct=True)).annotate(rep=Count('replies')).order_by('-created_at')
    return liked_threads


@login_required(login_url='/login')
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.updated_at = None
            thread.save()
            return redirect('forum:forum')
    else:
        form = ThreadForm()

    return render(request, 'create_thread.html', {'page_title': 'Create Thread', 'form': form})


@csrf_exempt
def create_thread_json(request):
    response_data = {'status': False}

    if request.method == 'POST':
        data = json.loads(request.body)

        print(data)
        new_thread = Thread.objects.create(
            title=data["title"],
            content=data["content"],

        )
        new_thread.created_by = get_user(request)
        new_thread.updated_at = None

        new_thread.save()

        response_data['status'] = True

    return JsonResponse(response_data)


@login_required(login_url='/login')
def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = Reply.objects.filter(thread=thread).all()
    likes = Like.objects.filter(thread=thread).all()
    form = RepliesForm(request.POST, error_class=DivErrorList)
    user_liked = Like.objects.filter(
        thread=thread, created_by=request.user).exists()
    return render(request, 'view_thread.html', {'page_title': thread.title + " - Forum", 'thread': thread, 'form': form, 'replies': replies, 'likes': likes, 'liked': user_liked})


@csrf_exempt
def view_thread_json(request, thread_id):
    response_data = {'status': False, 'data': {}, 'is_admin':  False}

    user = get_user(request)
    response_data['is_admin'] = user.is_staff
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = Reply.objects.filter(thread=thread).all()
    likes = Like.objects.filter(thread=thread).all()
    form = RepliesForm(request.POST, error_class=DivErrorList)
    user_liked = Like.objects.filter(
        thread=thread, created_by=get_user(request)).exists()

    # Populate response_data with relevant information
    response_data['status'] = True
    response_data['data']['title'] = remove_parentheses(thread.title)
    response_data['data']['thread_content'] = remove_parentheses(
        thread.content)
    response_data['data']['replies'] = [
        {'content': reply.content, 'created_by': reply.created_by.username, 'created_at': reply.created_at} for reply in replies]
    response_data['data']['likes'] = [
        {'created_by': like.created_by.username} for like in likes]
    response_data['data']['user_liked'] = user_liked

    return JsonResponse(response_data)


@login_required(login_url='/login')
def reply_to_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = RepliesForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            replies = form.save(commit=False)
            replies.thread = thread
            replies.created_by = request.user
            replies.save()

    return redirect('forum:view_thread', thread_id=thread.id)


@csrf_exempt
def reply_to_thread_json(request, thread_id):
    response_data = {'status': False}
    thread = get_object_or_404(Thread, pk=thread_id)

    print("masuk sini gasi")
    if request.method == 'POST':
        data = json.loads(request.body)

        print(data)
        print(thread.id)
        new_reply = Reply.objects.create(
            content=data["content"],
            thread=thread,

        )

        new_reply.created_by = get_user(request)

        new_reply.save()

        response_data['status'] = True

    return JsonResponse(response_data)


@login_required(login_url='/login')
def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.user == thread.created_by:
        if request.method == 'POST':
            form = ThreadForm(request.POST, instance=thread)
            if form.is_valid():
                form.save()
                return redirect('/forum', thread_id=thread.id)
        else:
            form = ThreadForm(instance=thread)
        return render(request, 'edit_thread.html', {'page_title': 'Edit Thread', 'form': form})
    else:
        return redirect('/forum', thread_id=thread.id)


@csrf_exempt
def edit_thread_json(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    user = get_user(request)
    response_data = {'status': False}
    if user == thread.created_by:

        if request.method == 'POST':
            data = json.loads(request.body)

            thread.title = remove_parentheses(data['title'])
            thread.content = remove_parentheses(data['content'])
            thread.save()
            response_data['status'] = True

    return JsonResponse(response_data)


@login_required(login_url='/login')
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.user == thread.created_by:
        thread.delete()
        return redirect('/forum')
    else:
        return redirect('/forum', thread_id=thread.id)


@csrf_exempt
def delete_thread_json(request, thread_id):
    response_data = {'status': False}
    user = get_user(request)
    thread = get_object_or_404(Thread, pk=thread_id)

    if user == thread.created_by:
        thread.delete()
        response_data['status'] = True
    # Tidak perlu else karena jika kondisi di atas tidak terpenuhi, status sudah False

    return JsonResponse(response_data)


@login_required(login_url='/login')
def like_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    user = request.user
    response_data = {'liked': False, 'likes_count': 0}

    if request.method == 'POST':
        existing_like = Like.objects.filter(
            thread=thread, created_by=user).first()

        if existing_like:
            # If it exists, delete it
            existing_like.delete()
            liked_status = False
        else:
            # Otherwise, create a new like
            Like.objects.create(thread=thread, created_by=user)
            liked_status = True

    # Count the current number of likes
    likes_count = thread.like_set.count()

    return JsonResponse({'liked': liked_status, 'likes_count': likes_count})


@csrf_exempt
def like_thread_json(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    user = get_user(request)
    response_data = {'liked': False, 'likes_count': 0}

    if request.method == 'POST':
        existing_like = Like.objects.filter(
            thread=thread, created_by=user).first()

        if existing_like:
            # If it exists, delete it
            existing_like.delete()
            liked_status = False
        else:
            # Otherwise, create a new like
            Like.objects.create(thread=thread, created_by=user)
            liked_status = True

    # Count the current number of likes
    likes_count = thread.like_set.count()

    return JsonResponse({'liked': liked_status, 'likes_count': likes_count})


def remove_parentheses(input_str):
    # Menghapus "('" di awal string
    if input_str.startswith("('"):
        input_str = input_str[2:]

    # Menghapus "',')" di akhir string
    if input_str.endswith("',)"):
        input_str = input_str[:-4]

    return input_str
