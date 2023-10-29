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
    return render(request, 'forum.html', {'page_title': 'Forum', 'threads': threads})


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


@login_required(login_url='/login')
def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = Reply.objects.filter(thread=thread).all()
    likes = Like.objects.filter(thread=thread).all()
    form = RepliesForm(request.POST, error_class=DivErrorList)
    user_liked = Like.objects.filter(thread=thread, created_by=request.user).exists()
    return render(request, 'view_thread.html', {'page_title': thread.title + " - Forum", 'thread': thread, 'form': form, 'replies': replies, 'likes': likes, 'liked': user_liked})


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
    

@login_required(login_url='/login')
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.user == thread.created_by:
        thread.delete()
        return redirect('/forum')
    else:
        return redirect('/forum', thread_id=thread.id)
    

@login_required(login_url='/login')
def like_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    user = request.user
    response_data = {'liked': False, 'likes_count': 0}

    if request.method == 'POST':
        existing_like = Like.objects.filter(thread=thread, created_by=user).first()

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


