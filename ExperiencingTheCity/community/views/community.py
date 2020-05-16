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

    if request.POST.get("isComplaint", "") == "0":
        pt.complaint = True
    else:
        pt.complaint = False

    pt.save()
    return HttpResponseRedirect(reverse('community:community_detail', args=(communityId,)))


## GET POST TYPES

def getPostTypes(request, id, activeStatus):
    communityPostTypes = PostType.objects.filter(community_id=id)
    context = {'communityPostTypes': communityPostTypes, 'communityActive': activeStatus}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, "PostTypeList.html", context)


def getPostType(request, id, activeStatus):
    print("=====================")
    print(id)
    post_type = get_object_or_404(PostType, pk=id)
    context = {'post_type': post_type, 'communityActive': activeStatus}
    if request.user.is_authenticated:
        user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = user
    return render(request, "PostType.html", context)


def archiveCommunity(request, id):
    community = get_object_or_404(Community, pk=id)
    community.active = False
    community.save()
    context = {'communityDetail': community}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return HttpResponseRedirect(reverse('community:home'))


## POST OPERATIONS

def new_post(request, id):
    post_type = get_object_or_404(PostType, pk=id)

    if post_type.formfields:
        form_fields = json.loads(post_type.formfields)
    else:
        form_fields = []
    context = {'post_type': post_type, "form_fields": form_fields}
    if request.user.is_authenticated:
        user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = user
    return render(request, "PostCreate.html", context)


def create_post(request, id):
    post_type = get_object_or_404(PostType, pk=id)

    community = post_type.community_id
    name = str(request.POST.get('name', "")).strip()
    query = str(request.POST.get('tags', "")).strip()
    description = str(request.POST.get('description', "")).strip()
    context = {'post_name': name, 'description': description}
    is_complaint = False
    complaint_status = ""
    wiki_tags = {}
    column_names = ("fieldposnr", "fieldlabel", "fieldtype", "enumvals", "isRequired", "fieldValue")
    json_response = {}

    if (post_type.complaint == True):
        is_complaint = True
        complaint_status = "Open"

    if (post_type.name != 'Generic Post Type' and post_type.name != 'Generic Post Type for Complaints'):
        form_fields = json.loads(post_type.formfields)
        for (k, v) in form_fields.items():
            for (key, value) in v.items():
                fieldposnr = value["fieldposnr"]
                fieldlabel = value["fieldlabel"]
                fieldtype = value["fieldtype"]
                enumvals = value["enumvals"]
                isRequired = value["isRequired"]
                fieldValue = str(request.POST.get(value["fieldlabel"], "")).strip()

                if fieldposnr not in json_response:
                    json_response[fieldposnr] = []

                json_element = {}
                json_element[column_names[0]] = fieldposnr
                json_element[column_names[1]] = fieldlabel
                json_element[column_names[2]] = fieldtype
                json_element[column_names[3]] = enumvals
                json_element[column_names[4]] = isRequired
                json_element[column_names[5]] = fieldValue

                json_response[fieldposnr].append(json_element)

    if name == "" or description == "":
        return HttpResponseRedirect(reverse('community:new_post', args=(id,)))

    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('community:home'))

    # if "get_tag" in request.POST:
    #   if query == "":
    #        context["error_message"] = "You need to enter a query to get tag suggestions."
    #        return HttpResponseRedirect(reverse('community:new_post', args=(id,)))
    #        #return render(request, 'PostCreate.html/' + id, context)
    #    else:
    #        suggested_tags = wiki_data.suggest_tags(query)
    #        if suggested_tags:
    #            context["suggested_tags"] = suggested_tags
    #        return HttpResponseRedirect(reverse('community:new_post', args=(id,)))

    # return render(request, 'PostCreate.html/' + id, context)

    # if "wiki_tag" in request.POST:
    #    wiki_tags["tags"] = []
    #    tags = request.POST.getlist('wiki_tag', "")
    #
    #    for i in range(len(tags)):
    #        wiki_tags["tags"].append(json.loads(tags[i].replace("\'", "\"")))

    else:
        post = Post(name=name, description=description, user_id=User.objects.get(username=request.user),
                    creation_date=timezone.now(), community_id=community,
                    form_fields=json.dumps(json_response), posttype_id=post_type, complaint=is_complaint,
                    complaint_status=complaint_status)
        post.save()

        return HttpResponseRedirect(reverse('community:home'))


def getPosts(request, id):
    print("======================")
    print(id)
    communityPosts = Post.objects.filter(community_id=id)
    context = {'communityPosts': communityPosts}

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user

    return render(request, "PostList.html", context)


def getPostDetail(request, id):
    post = get_object_or_404(Post, pk=id)
    post_type = post.posttype_id
    # comments = get_object_or_404(Comments, post_id=id)

    # context = {'post': post, 'post_type': post_type, 'comments':comments}
    if post.form_fields:
        form_fields = json.loads(post.form_fields)
    else:
        form_fields = []

    context = {'post': post, 'post_type': post_type, 'form_fields': form_fields}

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user

    return render(request, "PostDetail.html", context)
