from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, \
    UserAdditionalInfo, Followership
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
from ..utils import wiki_data
from django.db.models import Q


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
    context = {'communityDetail': communityDetail}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, "CommunityDetail.html", context)


def getCommunityByFilter(request):
    filterString = request.GET.get("filterString", "")
    communities = list(
        Community.objects.filter(
            Q(name__icontains=filterString) | Q(tags__tags__0__label__contains=filterString)).values())
    # Q(name__icontains=filterString) | Q(tags__contains=[{"tags": [{"label": filterString}]}])).values())
    return JsonResponse({"communities": communities}, safe=False)


def getCommunityListByFilter(request):
    idList = request.GET.getlist("idList[]", "")
    print("==============")
    print(idList)
    community_list = Community.objects.filter(id__in=idList)
    print(community_list)
    context = {'community_list': community_list}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, 'Home.html', context)


def getCommunityHeader(request, id):
    communityDetail = get_object_or_404(Community, pk=id)
    return render(request, "PostType.html", {"communityDetail": communityDetail})


# NEW COMMUNITY

def new_community(request):
    if not request.user.is_authenticated:
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
    query = str(request.POST.get('tags', "")).strip()
    description = str(request.POST.get('description', "")).strip()
    context = {'community_name': name, 'description': description}
    lat = request.POST.getlist('latitude', "")
    lon = request.POST.getlist('longitude', "")
    geolocation = {"location": []}
    for i in range(len(lat)):
        geolocation["location"].append({"lat": lat[i], "lon": lon[i]})  # TODO: error handling for no location
    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('community:home'))
    if "get_tag" in request.POST:
        if query == "":
            context["error_message"] = "You need to enter a query to get tag suggestions."
            return render(request, 'CommunityCreate.html', context)
        else:
            suggested_tags = wiki_data.suggest_tags(query)
            if suggested_tags:
                context["suggested_tags"] = suggested_tags
            return render(request, 'CommunityCreate.html', context)
    try:
        old_community = Community.objects.get(name=name)
    except:
        old_community = None
    if old_community:
        return render(request, 'CommunityCreate.html', {
            'error_message': "There is another community named " + name,
            'description': description
        })
    wiki_tags = {}
    if "wiki_tag" in request.POST:
        wiki_tags["tags"] = []
        tags = request.POST.getlist('wiki_tag', "")
        for i in range(len(tags)):
            wiki_tags["tags"].append(json.loads(tags[i].replace("\'", "\"")))  # TODO: error handling for empty tags
    community = Community(name=name, description=description, creation_date=datetime.datetime.now(), active=True,
                          owner=request.user, geolocation=geolocation, tags=wiki_tags)
    if community.name == "" or community.description == "":
        return render(request, 'CommunityCreate.html', {
            'error_message': "Name, Description or Tag fields cannot be empty.",
            'description': description,
            'community_name': name
        })
    else:
        community.save()

        # Generic Post Type creation
        pt = PostType()
        pt.community_id = Community.objects.get(pk=community.id)
        pt.name = "Generic Post Type"
        pt.description = "Here is a generic post type for your basic posts in the community!"
        pt.owner = User.objects.get(username=request.user)
        pt.creation_date = datetime.datetime.now()
        pt.save()

        # Generic Complaint Post Type creation
        pt = PostType()
        pt.community_id = Community.objects.get(pk=community.id)
        pt.name = "Generic Post Type for Complaints"
        pt.description = "Here is a generic post type for your complaint posts in the community!"
        pt.owner = User.objects.get(username=request.user)
        pt.creation_date = datetime.datetime.now()
        pt.creation_date = datetime.datetime.now()
        pt.complaint = True;
        pt.save()
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
    return HttpResponseRedirect(reverse('community:community_detail', args=(communityId,)))


## GET POST TYPES

def getPostTypes(request, id):
    communityPostTypes = PostType.objects.filter(community_id=id)
    context = {'communityPostTypes': communityPostTypes}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, "PostTypeList.html", context)


def getPostType(request, id):
    post_type = get_object_or_404(PostType, pk=id)
    context = {'post_type': post_type}
    if request.user.is_authenticated:
        user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = user
    return render(request, "PostType.html", context)
