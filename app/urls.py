from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include('social_django.urls')),
    path('', main),
    path('logout/', logout_v, name='logout_url')
]
