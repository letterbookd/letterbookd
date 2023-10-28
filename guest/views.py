from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forum.views import user_thread_data, user_liked_thread_data


from reader.models import *
from library.models import Library

# Views for Guest
def show_landing(request):
    return render(request, 'main.html', context={})

def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("library:show_library"))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("library:show_library"))  ## TODO: ganti jadi library 
            return response
        else:
            messages.info(request, 'Incorrect username or password')
    context = {'page_title': "Sign in"}
    return render(request, 'login.html', context)

def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("library:show_library"))
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            # buat objek reader juga
            reader = Reader()
            reader.user = user
            reader.display_name = user.get_username()
            reader.personal_library = Library()
            reader.preferences = ReaderPreferences()
            reader.personal_library.save()
            reader.preferences.save()
            reader.save()

            response = HttpResponseRedirect(reverse("library:show_library"))
            return response
    context = {'page_title': "Sign up"}
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('guest:landing_page'))
    return response



