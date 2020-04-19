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


def homepage(request):
    context = {}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context = {
            'user': community_user
        }
    return render(request, 'Home.html', context)
