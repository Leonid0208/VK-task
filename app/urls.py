from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', include('social_django.urls')),
    path('', process_main_page),
    path('logout/', logout_v, name='logout_url'),
    path('show-users/', show_friends, name='show_users'),
    path('login/', login_user, name='login')
]
