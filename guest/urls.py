from django.urls import path
from guest.views import *

app_name = 'guest'

urlpatterns = [
    path('', show_landing, name='landing_page'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    
]