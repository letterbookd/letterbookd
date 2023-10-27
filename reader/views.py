from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reader
from .forms import ReaderForm, ReaderPreferencesForm
from django.contrib.auth.models import User
from library.models import *
from catalog.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

# Menampilkan halaman profile Reader
def show_profile(request, id):
    reader = get_object_or_404(Reader, user__id=id)
    return render(request, 'profile.html', {'reader': reader, 'page_title': 'Profile'})

# Mengembalikan halaman hasil searching Reader dengan display_name
def search_reader(request, display_name):
    readers = Reader.objects.filter(display_name__icontains=display_name)
    return render(request, 'user_search_results.html', {'readers': readers})

# Mengedit profil (display_name dan bio) user dari halaman profilenya
def edit_profile(request, user_id):
    if request.method == 'POST':
        reader = get_object_or_404(Reader, user__id=user_id)
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'There was an error updating the profile'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Render halaman setting untuk Reader
def user_settings(request):
    reader = get_object_or_404(Reader, user=request.user)
    
    reader_form = ReaderForm(instance=reader)
    preferences_form = ReaderPreferencesForm(instance=reader.preferences)

    context = {
        'reader_form': reader_form,
        'preferences_form': preferences_form
    }
    
    return render(request, 'user_settings.html', context)


# Menampilkan hasil searching buku untuk suatu reader di catalog
def search_catalog(request):
    query = request.GET.get('q')
    results = Book.objects.filter(title__icontains=query)
    return render(request, 'book_search_results.html', {'results': results})

# Menampilkan hasil searching buku untuk suatu reader di library
def search_library(request):
    query = request.GET.get('q')
    user_books = LibraryBook.objects.filter(user=request.user, book__title__icontains=query)
    return render(request, 'book_search_results.html', {'results': user_books})

def show_json(request):
    all_readers = Reader.objects.all()
    return HttpResponse(serializers.serialize("json", all_readers), content_type="application/json")

def show_json_by_id(request, id):
    specific_reader = Reader.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", specific_reader), content_type="application/json")

def get_all_readers_json(request):
    all_readers = Reader.objects.all()
    return HttpResponse(serializers.serialize('json', all_readers))

@csrf_exempt
def edit_profile_ajax(request, id):
    if request.method == 'POST':
        display_name = request.POST.get("display_name")
        bio = request.POST.get("bio")

        reader = Reader.objects.get(pk = id)

        reader.display_name = display_name
        reader.bio = bio
   
        reader.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
