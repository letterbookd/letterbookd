import json
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from review.models import Review
from .models import Reader, ReaderPreferences
from .forms import ReaderForm, ReaderPreferencesForm, UserProfileForm
from django.contrib.auth.models import User
from library.models import *
from catalog.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .serializers import ReaderSerializer



# Menampilkan halaman profile Reader
'''
def show_profile(request, id):
    reader = get_object_or_404(Reader, user__id=id)
    return render(request, 'profile.html', {'reader': reader, 'page_title': 'Profile'})
'''

'''
@login_required(login_url='/login')
def show_profile(request, id):
    # Dapatkan objek reader
    reader = get_object_or_404(Reader, user__id=id)

    # Dapatkan semua buku di library pengguna
    library_books = LibraryBook.objects.filter(library__reader=reader)

    context = {
        'reader': reader,
        'page_title': "Profile",
        'library_books': library_books,
    }

    return render(request, 'profile.html', context)
'''

@login_required(login_url='/login')
def show_profile(request, id):
    # Dapatkan objek reader
    reader = get_object_or_404(Reader, user__id=id)

    # Dapatkan semua buku di library pengguna
    library_items = get_object_or_404(Library, reader__user__id=id).mybooks.order_by('-id').all()

    # Dapatkan semua review yang ditulis pengguna
    reviews = Review.objects.filter(user=reader)

    form = UserProfileForm()

    context = {
        'reader': reader,
        'page_title': "Profile",
        'library_items': library_items,
        'form': form,
        'reviews': reviews, 
    }

    return render(request, 'profile.html', context)



# Mengembalikan halaman hasil searching Reader dengan display_name
def search_reader(request, display_name):
    readers = Reader.objects.filter(display_name__icontains=display_name)
    return render(request, 'user_search_results.html', {'readers': readers, 'page_title': "Reader Search"})

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
    specific_reader = Reader.objects.filter(user__id=id).first()
    if specific_reader is not None:
        # Fetch the associated ReaderPreferences
        reader_preferences = specific_reader.preferences

        # Extract the 'share_reviews' field from ReaderPreferences
        share_reviews = reader_preferences.share_reviews
        share_library = reader_preferences.share_library

        # Create a dictionary containing the relevant data
        response_data = {
            'id': specific_reader.id,
            'username': specific_reader.user.username,
            'bio': specific_reader.bio,
            'display_name': specific_reader.display_name,
            'share_reviews': share_reviews,
            'share_library': share_library,
        }

        return JsonResponse(response_data)
    else:
        # Handle the case when the specific_reader is not found
        return JsonResponse({'error': 'Reader not found'}, status=404)

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

        share_reviews = request.POST.get("share_reviews") == "on"
        share_library = request.POST.get("share_library") == "on"
        
        reader = get_object_or_404(Reader, user__id=id)

        reader.display_name = display_name
        reader.bio = bio
    
        # Dapatkan semua buku di library pengguna
        
        reader.preferences.share_reviews = share_reviews
        reader.preferences.share_library = share_library
        reader.preferences.save()

        #
        reader.save()

        return HttpResponse("CREATED", status=201)

    return HttpResponseNotFound()

# Mencari di catalog/library/reader
def search_handler(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')

    if search_type == "catalog":
        results = Book.objects.filter(title__icontains=query)
        return render(request, 'catalog_search_results.html', {'results': results, 'query': query})

    elif search_type == "library":
        user_books = LibraryBook.objects.filter(library__reader__user=request.user, book__title__icontains=query)
        return render(request, 'library_search_results.html', {'results': user_books, 'query': query})


    elif search_type == "reader":
        readers = Reader.objects.filter(Q(display_name__icontains=query) | Q(user__username__icontains=query))
        return render(request, 'user_search_results.html', {'readers': readers, 'query': query})

    else:
        return HttpResponse("Invalid search type.")

@login_required(login_url='/login')
def show_user_library(request):
    ''' Menampilkan semua buku di library milik user '''
    
    # Dapatkan library milik user
    user_library = get_object_or_404(Library, reader__user=request.user) 
    
    # Dapatkan semua LibraryBook yang terkait dengan library user tersebut
    user_library_books = user_library.mybooks.all()
    
    # Dapatkan semua buku dari setiap LibraryBook
    books_in_library = [lib_book.book for lib_book in user_library_books]

    context = {
        'page_title': "My Library",
        'books': books_in_library,
        'display_name': get_object_or_404(Reader, user=request.user).display_name, 
    }
    return render(request, './user_library.html', context)


def get_reader_json(request):
    try:
        username = request.headers['username']
        user = get_object_or_404(User, username=username)
        reader = get_object_or_404(Reader, user__id=user.id)

        reader_data = {
            'display_name': reader.display_name,
            'bio': reader.bio,
            'profile_picture': reader.profile_picture,
            'preferences': {
                'share_reviews': reader.preferences.share_reviews,
                'share_library': reader.preferences.share_library
            }
        }
        return JsonResponse(reader_data)
    except Reader.DoesNotExist or ReaderPreferences.DoesNotExist:
        return JsonResponse({'error': 'Data not found'}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
def get_readers_json(request):
    readers = list(Reader.objects.values())  
    reader_preferences = list(ReaderPreferences.objects.values())  

    combined_data = {
        'readers': readers,
        'reader_preferences': reader_preferences
    }

    return JsonResponse(combined_data)


def search_readers_api(request):
    def format_reader_data(reader):
        return {
        'display_name': reader.display_name,
        'bio': reader.bio,
        'profile_picture': reader.profile_picture,
        'preferences': {
            'share_reviews': reader.preferences.share_reviews,
            'share_library': reader.preferences.share_library
        }
    }
    try:
        query = request.GET.get('q')
        if query:
            readers = Reader.objects.filter(Q(display_name__icontains=query) | Q(user__username__icontains=query))
            serializer = [format_reader_data(reader) for reader in readers]

            return JsonResponse(serializer, safe=False)
        else:
            return JsonResponse({'error': 'Invalid or empty query'})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def update_profile(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request"})

    try:
        data = json.loads(request.body)
        print("Received data:", data)

        with transaction.atomic():
            user = User.objects.get(username=data.get('username'))

            share_reviews = data.get("share_reviews", False)
            share_library = data.get("share_library", False)
            
            reader_profile = get_object_or_404(Reader, user__id=user.id)

            reader_profile.display_name = data.get('display_name', reader_profile.display_name)
            reader_profile.bio = data.get('bio', reader_profile.bio)
            
            reader_profile.preferences.share_reviews = share_reviews
            reader_profile.preferences.share_library = share_library
            reader_profile.preferences.save()

            reader_profile.save()

        return JsonResponse({"status": "success", "message": "Profile updated successfully"})

    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

# ======================

def reader_library_api(request, username):
    # Dapatkan objek reader berdasarkan username
    reader = get_object_or_404(Reader, user__username=username)

    # Dapatkan semua buku di library pengguna
    library_items = LibraryBook.objects.filter(library__reader=reader)

    # Format data buku menjadi JSON
    books_json = [{
        'title': item.book.title,
        'authors': item.book.authors,
        'thumbnail': item.book.thumbnail if item.book.thumbnail else None,  
    } for item in library_items]

    return JsonResponse(books_json, safe=False)

