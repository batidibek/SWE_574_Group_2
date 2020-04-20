from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, \
    UserAdditionalInfo, Followership, City
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
from django.utils import timezone

# COMMUNITY LIST

def community_list(request):
    community_list = Community.objects.order_by('-creation_date')[:30]
    context = {'community_list': community_list}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, 'Communities.html', context)


def getCommunity(request, id):
    communityDetail = get_object_or_404(Community, pk=id)
    communityDataTypes = PostType.objects.filter(community_id=id)
    communityPosts = Post.objects.filter(community_id=id)
    print(SemanticTags.objects.filter(community_id=id, post_id=0))
    tmpObj = serializers.serialize("json", SemanticTags.objects.filter(community_id=id, post_id=0).only("tag_info"))
    print("---------------------------------")
    print(tmpObj)

    communityTags = json.loads(tmpObj)
    return render(request, "CommunityDetail.html", {"communityDetail": communityDetail,
                                                    "communityDataTypes": communityDataTypes,
                                                    "communityTags": communityTags,
                                                    "communityPosts": communityPosts})


def getCommunityHeader(request, id):
    communityDetail = get_object_or_404(Community, pk=id)
    return render(request, "PostType.html", {"communityDetail": communityDetail})


# NEW COMMUNITY

def new_community(request):
    if not request.user.is_authenticated:
        community_list = Community.objects.order_by('-pub_date')[:30]
        return render(request, 'Home.html', {
            'error_message': "You need to Log in or Sign up to create new community.",
        })
    else:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        return render(request, 'CommunityCreate.html', {'user': community_user})


def create_community(request):
    print(request.POST)
    if not request.user.is_authenticated:
        community_list = Community.objects.order_by('-pub_date')[:30]
        return render(request, 'Home.html', {
            'community_list': community_list,
            'error_message': "You need to Log in or Sign up to create new community.",
        })
    name = str(request.POST.get('name', "")).strip()
    description = str(request.POST.get('description', "")).strip()
    city = str(request.POST.get('city', "")).strip()
    country = str(request.POST.get('country', "")).strip()
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('community:home'))
    if city == "":
        return render(request, 'CommunityCreate.html', {
            'error_message': "You must select a city.",
            'description': description,
            'community_name': name
        })
    try:
        city_object = City.objects.get(name=city)
        try:
            old_community = Community.objects.get(name=name, city=city_object)
        except:
            old_community = None
        if old_community:
            return render(request, 'CommunityCreate.html', {
                'error_message': "There is another community named " + name + " in " + city_object.name,
                'description': description
            })
    except:
        city_object = City(name=city, country=country)
    community = Community(name=name, description=description, creation_date=datetime.datetime.now(), active=True,
                          owner=request.user, city=city_object)
    if community.name == "" or community.description == "" or request.POST['tags'] == "":
        return render(request, 'CommunityCreate.html', {
            'error_message': "Name, Description or Tag fields cannot be empty.",
            'description': description,
            'community_name': name
        })
    else:
        city_object.save()
        community.save()
        return HttpResponseRedirect(reverse('community:home'))


## NEW POST TYPE

def newPostType(request):
    fieldJson = request.POST.get("postTypeFields", "")
    print(fieldJson)
    communityId = request.POST.get("communityId", "")

    pt = PostType()
    pt.community_id = Community.objects.get(pk=communityId)
    pt.name = request.POST.get("PostTypeName", "")
    pt.description = request.POST.get("PostTypeDescription", "")
    pt.owner_id = User.objects.get(username=request.user).id
    pt.formfields = fieldJson
    pt.creation_date = timezone.now()
    pt.complaint = False;
    pt.save()

    # return HttpResponse(dt.pk)
    return redirect('/communities/' + communityId)
