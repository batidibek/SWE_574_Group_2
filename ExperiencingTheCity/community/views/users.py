from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, UserAdditionalInfo, Followership, City
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

#SIGN UP

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

#SIGN IN

def sign_in(request):
   return render(request, 'SignIn.html')            

def authenticate_user(request):
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('community:home'))
    user_key = request.POST["user_key"]
    password = request.POST["password"] 
    if user_key == "" or password == "":
        return render(request, 'SignIn.html', {
            'error_message': "Please provide your username or email adress, and password.",
        })
    username_checker = False
    try:
        u = User.objects.get(username=user_key)
    except:
        username_checker = True
    email_checker = False
    try:
        u = User.objects.get(email=user_key)
        user_key = u.username
    except:
        email_checker = True
    if username_checker and email_checker:
       return render(request, 'SignIn.html', {
            'error_message': "This username or email adress does not exist.",
        })         
    user = authenticate(request, username=user_key, password=password)    
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('community:home'))
    else:
        return render(request, 'SignIn.html', {
        'error_message': "Invalid password.",
    })   

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('community:home'))    