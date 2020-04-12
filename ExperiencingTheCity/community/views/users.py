from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, UserAdditionalInfo, Followership
from django.http import Http404
from django.urls import reverse
import datetime
import json
import uuid
from django.core import serializers
from django.http import JsonResponse
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import requests

def sign_up(request):
    return render(request, 'SignUp.html')

def create_user(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('home'))
    username = request.POST["username"] 
    email = request.POST["email"]
    password = request.POST["password"]   
    if " " in username:
        return render(request, 'SignUp.html', {
            'error_message': "You cannot use blank space in username.",
        })
    if username == "" or email == "" or password == "":
        return render(request, 'SignUp.html', {
            'error_message': "You cannot leave username, mail adress and password fields empty.",
        })
    if len(password) < 8:
        return render(request, 'SignUp.html', {
            'error_message': "Your password should contain at least 8 characters.",
        })    
    username_checker = True
    try:
        u = User.objects.get(username=username)
    except:
        username_checker = False
    if username_checker:
        return render(request, 'SignUp.html', {
            'error_message': "This username is already taken.",
        })
    email_checker = True    
    try:
        u = User.objects.get(email=email)
    except:
        email_checker = False
    if email_checker:
        return render(request, 'SignUp.html', {
            'error_message': "This email adress has an account.",
        })
    user = User.objects.create_user(username=username, email=email, password=password)     
    user.save()
    login(request, user)
    community_user = UserAdditionalInfo(user=user)
    community_user.save()
    return HttpResponseRedirect(reverse('community:home'))       
