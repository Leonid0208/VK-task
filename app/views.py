from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
import requests
from django.contrib.auth import authenticate, login, logout
from .models import *


def main(request):
    code = request.GET.get('code', '')

    if code:
        token = requests.get('https://oauth.vk.com/access_token?client_id=7549290&client_secret=IC1EzUqnxGJFJqeMyn4h&redirect_uri=https://vk-friends-task.herokuapp.com/&code={}'.format(code))
        id = token.json()['user_id']
        access_token = token.json()['access_token']

        name_user = requests.get('https://api.vk.com/method/users.get', {
            'user_id': id,
            'v': 5.52,
            'fields': 'photo_200',
            'access_token': access_token,
        })
        if not User.objects.filter(username=id).exists():
            User.objects.create(username=id)
            user = User.objects.get(username=id)
            user.profile.access_token = access_token
            user.first_name = name_user.json()['response'][0]['first_name']
            user.last_name = name_user.json()['response'][0]['last_name']
            user.profile.photo = name_user.json()['response'][0]['photo_200']
            user.save()
        else:
            user = User.objects.get(username=id)
            user.profile.access_token = access_token
            user.save()
        user = authenticate(request, username=id)
        login(request, user)

        return HttpResponseRedirect('/')

    if request.user.is_authenticated:
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
        print(friends.json()['response']['items'])
        return render(request, 'app/base_app.html', {'friends_list': friends.json()['response']['items']})
    return render(request, 'app/base_app.html')


def logout_v(request):
    logout(request)
    return HttpResponseRedirect('/')
