from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reader
from .forms import ReaderForm, ReaderPreferencesForm
from django.contrib.auth.models import User
from library.models import *
from catalog.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q

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


# Menampilkan data JSON readers 
def show_json(request):
    all_readers = Reader.objects.all()
    return HttpResponse(serializers.serialize("json", all_readers), content_type="application/json")

# Menampilkan data JSON specific reader berdasarkan ID 
def show_json_by_id(request, id):
    specific_reader = Reader.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", specific_reader), content_type="application/json")

# Mendapatkan data JSON readers
def get_all_readers_json(request):
    all_readers = Reader.objects.all()
    return HttpResponse(serializers.serialize('json', all_readers))

# Mengubah profile reader
@csrf_exempt
def edit_profile_ajax(request, id):
    if request.method == 'POST':
        display_name = request.POST.get("display_name")
        bio = request.POST.get("bio")
        
        # NYOBA BARU
        share_reviews = request.POST.get("share_reviews")
        share_library = request.POST.get("share_library")
        #

        reader = Reader.objects.get(pk = id)

        reader.display_name = display_name
        reader.bio = bio
        
        # NYOBA BARU
        reader.share_reviews = share_reviews
        reader.share_library = share_library
        #

        reader.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

# Mencari di catalog/library/reader
def search_handler(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')

    if search_type == "catalog":
        results = Book.objects.filter(title__icontains=query)
        return render(request, 'book_search_results.html', {'results': results})

    elif search_type == "library": # INI MASIH ERROR
        user_books = LibraryBook.objects.filter(user=request.user, book__title__icontains=query)
        #user_books = LibraryBook.objects.filter(library__user=request.user, book__title__icontains=query)
        return render(request, 'book_search_results.html', {'results': user_books})

    elif search_type == "reader":
        readers = Reader.objects.filter(Q(display_name__icontains=query) | Q(user__username__icontains=query))
        return render(request, 'user_search_results.html', {'readers': readers})

    else:
        return HttpResponse("Invalid search type.")