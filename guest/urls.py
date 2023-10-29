from django.urls import path
from guest.views import *

app_name = 'guest'

urlpatterns = [
    path('', show_landing, name='landing_page'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
<<<<<<< HEAD
=======
    
>>>>>>> 26a5480b63896b7f2ead40c11a9bcf920241ce6d
]