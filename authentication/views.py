from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from guest.forms import PrettierUserCreationForm
from reader.models import Reader, ReaderPreferences
from library.models import Library

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "librarian": hasattr(user, "librarian"),
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali username dan password."
        }, status=401)
    
@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = PrettierUserCreationForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()

            # buat objek reader juga
            reader = Reader()
            reader.user = new_user
            reader.display_name = new_user.get_username()
            reader.personal_library = Library()
            reader.preferences = ReaderPreferences()
            reader.personal_library.save()
            reader.preferences.save()
            reader.save()

        return JsonResponse({"username": form.cleaned_data['username'], "status": True, "message": "Register successful!"}, status=201)
    else:
        return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)