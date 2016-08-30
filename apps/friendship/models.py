from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, conpass, bday):
        errors = []
        the_user = User.objects.filter(email = email)
        if len(name) < 1:
            errors.append('Name is wrong')
        if len(alias) < 1:
            errors.append('Alias is wrong')
        if not EMAIL_REGEX.match(email):
            errors.append('Invalid Email')
        if the_user:
            errors.append('Email already taken')
        if len(password) < 5:
            errors.append('Password is wrong')
        if conpass != password:
            errors.append('Passwords don\'t match')
        if len(errors) > 0:
            return errors
        else:
            return True

    def login(self, email, password):
        errors = []
        the_user = User.objects.filter(email = email)
        if the_user:
            if bcrypt.hashpw(password.encode('utf-8'), the_user[0].password.encode('utf-8')) == the_user[0].password:
                return True
            else:
                errors.append('Wrong email or password')
                return errors
        else:
            errors.append('Wrong email or password')
            return errors



class User(models.Model):
    name = models.CharField(max_length = 200)
    alias = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    bday = models.DateTimeField(max_length = 200)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name = 'user_to_friendship')
    friend = models.ForeignKey(User, related_name = 'friend_to_friendship')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
