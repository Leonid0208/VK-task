from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
import requests
from django.contrib.auth import authenticate, login, logout
from .models import *


def show_friends(request):
    user = request.user
    friends = requests.get('https://api.vk.com/method/friends.get', {
        'user_id': user.username,
        'v': 5.52,
        'fields': 'domain,photo',
        'order': 'name',
        'count': 5,
        'offset': 5,
        'access_token': user.profile.access_token,
    })
    return render(request, 'app/base.html', {'friends_list': friends.json()['response']['items']})


def login_user(request):
    code = request.GET.get('code', '')
    token = requests.get('https://oauth.vk.com/access_token?client_id=7549290&client_secret=IC1EzUqnxGJFJqeMyn4h&redirect_uri=https://vk-friends-task.herokuapp.com/login/&code={}'.format(code))
    json = token.json()
    id = json['user_id']
    access_token = json['access_token']

    name_user = requests.get('https://api.vk.com/method/users.get', {
        'user_id': id,
        'v': 5.52,
        'fields': 'photo_200',
        'access_token': access_token,
    })
    user_info = name_user.json()['response'][0]

    if not User.objects.filter(username=id).exists():    # регистрация польователя, если его нету в БД
        User.objects.create(username=id)
        user = User.objects.get(username=id)
        user.profile.access_token = access_token
        user.first_name = user_info['first_name']
        user.last_name = user_info['last_name']
        user.profile.photo = user_info['photo_200']
        user.save()
    else:                                                # обновление токена у существующего пользователя
        user = User.objects.get(username=id)
        user.profile.access_token = access_token
        user.save()
    user = authenticate(request, username=id)            # авторизация на сайт
    login(request, user)

    return HttpResponseRedirect('/')


def process_main_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('show-users/')
    return render(request, 'app/base.html')


def logout_v(request):
    logout(request)
    return HttpResponseRedirect('/')
