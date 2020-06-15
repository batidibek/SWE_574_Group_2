from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.template import loader, context
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, \
    UserAdditionalInfo, Followership, Action
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
from django.views.decorators.http import require_POST

# SIGN UP

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


# SIGN IN

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


## USER PROFILE

def user_profile(request, id):
    userProfile = get_object_or_404(User, pk=id)
    userCommunities = Community.objects.filter(owner=id)
    userPosts = Post.objects.filter(user_id=id)

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)

    return render(request, "UserProfile.html", {'userProfile': userProfile,
                                                'userCommunities': userCommunities,
                                                'userPosts': userPosts,
                                                'user': community_user})


def user_posts(request, id):
    userProfile = get_object_or_404(User, pk=id)
    userPosts = Post.objects.filter(user_id=id)

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)

    return render(request, "UserPosts.html", {'userProfile': userProfile,
                                              'userPosts': userPosts,
                                              'user': community_user})


def user_communities(request, id):
    userProfile = get_object_or_404(User, pk=id)
    userCommunities = Community.objects.filter(owner=id)

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)

    return render(request, "UserCommunities.html", {'userProfile': userProfile,
                                                    'userCommunities': userCommunities,
                                                    'user': community_user})


def user_list(request, id):
    userProfile = get_object_or_404(User, pk=id)
    users = User.objects.all()

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)

    return render(request, "UserFollows.html", {'userProfile': userProfile,
                                                'users': users,
                                                'user': community_user})


def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Followership.objects.get_or_create(
                    follows=request.user,
                    followed=user)
            else:
                Followership.objects.filter(follows=request.user,
                                            followed=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


def activity_stream(request, id):
    userProfile = get_object_or_404(User, pk=id)

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)

    action = Action.objects.all()

    return render(request, 'UserActivityStream.html', {'userProfile': userProfile,
                                                       'user': community_user,
                                                       'activity_stream': action})
