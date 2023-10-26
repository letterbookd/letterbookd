from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reader
from .forms import ReaderForm, ReaderPreferencesForm
from django.contrib.auth.models import User
from library.models import *
from catalog.models import *
from django.views.decorators.csrf import csrf_exempt

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

# Mengapply setting untuk Reader
def apply_settings(request):
    if request.method == 'POST':
        reader = get_object_or_404(Reader, user=request.user)
        reader_form = ReaderForm(request.POST, instance=reader)
        preferences_form = ReaderPreferencesForm(request.POST, instance=reader.preferences)
        
        if reader_form.is_valid() and preferences_form.is_valid():
            reader_form.save()
            preferences_form.save()
            return JsonResponse({'status': 'success', 'message': 'Settings applied successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'There was an error applying the settings'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


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

# Mengembalikan data akun Reader untuk digunakan dalam bentuk JSON
def get_reader_data_by_user(request, user_id):
    reader = get_object_or_404(Reader, user__id=user_id)
    
    preferences = reader.preferences
    
    reader_data = {
        'display_name': reader.display_name,
        'bio': reader.bio,
        'profile_picture': reader.profile_picture,
        'personal_library': reader.personal_library,
        'preferences': {
            'share_reviews': preferences.share_reviews,
            'share_library': preferences.share_library
        }
    }
    
    return JsonResponse(reader_data)

from django.http import JsonResponse

# Update data reader dengan AJAX 
@csrf_exempt
def update_reader_settings_ajax(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        display_name = request.POST.get("display_name")
        bio = request.POST.get("bio")
        profile_picture = request.POST.get("profile_picture")  
        share_reviews = request.POST.get("share_reviews") == 'true'  
        share_library = request.POST.get("share_library") == 'true' 
        
        try:
            reader = Reader.objects.get(user=request.user)
            
            reader.display_name = display_name
            reader.bio = bio
            reader.profile_picture = profile_picture
            reader.share_reviews = share_reviews
            reader.share_library = share_library

            reader.save()

            return JsonResponse({'status': 'success', 'message': 'Settings updated successfully'})

        except Reader.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Reader does not exist'}, status=404)
        except Exception as e: 
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)