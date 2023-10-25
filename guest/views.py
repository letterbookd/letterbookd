from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages  
from django.contrib.auth.decorators import login_required

# Views for Guest
def show_landing(request):
    return render(request, 'main.html', context={})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("guest:show_landing"))  ## TODO: ganti jadi library 
            return response
        else:
            messages.info(request, 'Incorrect username or password')
    context = {'page_title': "Sign in"}
    return render(request, 'login.html', context)

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            # TODO: buat biar langsung login dan ke library
            return redirect('guest:landing_page')
    context = {'page_title': "Sign up"}
    return render(request, 'register.html', context)


def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('guest:landing_page'))
    response.delete_cookie('last_login')
    return response