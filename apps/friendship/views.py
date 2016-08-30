from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Friendship, UserManager
from django.db.models import Q
import bcrypt
import datetime

def index(request):
    return render(request, 'friendship/index.html')

def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    conpass = request.POST['conpass']
    bday = request.POST['bday']
    check = User.objects.register(name, alias, email, password, conpass, bday)
    if check == True:
        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(name = name, alias = alias, email = email, password = pwhash, bday = bday)
        request.session['current_user'] = user.id
        return redirect('/friends')
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect('/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    check = User.objects.login(email, password)
    if check == True:
        user = User.objects.get(email = request.POST['email'])
        request.session['current_user'] = user.id
        return redirect('/friends')
    else:
        messages.warning(request, check[0])
        return redirect('/')

def logout(request):
    request.session['current_user'] = 0
    return redirect('/')

def friends(request):
    user = User.objects.get(id = request.session['current_user'])
    my_friends = User.objects.filter(friend_to_friendship__user__id = user.id)
    not_friends = User.objects.filter(~Q(friend_to_friendship__user__id = user.id)).filter(~Q(id = user.id))
    context = {'user':user, 'friends': my_friends, 'not_friends' : not_friends}
    return render(request, 'friendship/friends.html', context)

def addfriend(request, id):
    user = User.objects.get(id = request.session['current_user'])
    friend = User.objects.get(id = id)
    Friendship.objects.create(user = user, friend = friend)
    Friendship.objects.create(user = friend, friend = user)
    return redirect('/friends')

def remove(request, id):
    user = User.objects.get(id = request.session['current_user'])
    friend = User.objects.get(id = id)
    Friendship.objects.filter(user = user, friend = friend).delete()
    Friendship.objects.filter(user = friend, friend = user).delete()
    return redirect('/friends')

def user(request, id):
    user = User.objects.get(id = id)
    context = {'user':user}
    return render(request, 'friendship/user.html', context)
