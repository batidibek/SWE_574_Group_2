from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Community, PostType, Post, SemanticTags, MemberShip, Comments, InappropriatePosts, Notification, \
    UserAdditionalInfo, Followership, Action
from django.http import Http404
from django.urls import reverse
import datetime
from datetime import timedelta
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
from django.db.models import Q, Count
from django.core.files.storage import default_storage
from ..utils.activity_stream import create_action

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
    
    number_of_posts = Post.objects.filter(community_id=id).count()
    number_of_posttypes = PostType.objects.filter(community_id=id).count()

    context = {'communityDetail'     : communityDetail,
               'number_of_posts'     : number_of_posts,
               'number_of_posttypes' : number_of_posttypes}

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
    context = { "communityDetail": communityDetail }
    context["user"] = request.user
    return render(request, "PostType.html", {context})


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
    description = description[0 : 199]
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

        # user created community action for activity stream
        create_action(request.user, 'created a new community:', community)

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
        pt.complaint = True
        pt.save()
        return HttpResponseRedirect(reverse('community:home'))


## NEW POST TYPE

def newPostType(request):
    communityId = request.POST.get("communityId", "")
    postTypeId = request.POST.get("postTypeId", "")
    if "cancel" in request.POST:
        #  onclick="location.href='{% url 'community:post_types' communityDetail.id communityDetail.active %}'">
        return HttpResponseRedirect(reverse('community:post_types', args=(communityId, postTypeId,)))
    else:
        fieldJson = request.POST.get("postTypeFields", "")
        print(fieldJson)

        print(postTypeId)
        if (postTypeId != ''):
            pt = PostType.objects.get(pk=postTypeId)
        else:
            pt = PostType()
        pt.community_id = Community.objects.get(pk=communityId)
        pt.name = request.POST.get("PostTypeName", "")
        print(pt.name)
        pt.description = request.POST.get("PostTypeDescription", "")
        pt.description = pt.description[0: 199]
        pt.owner_id = User.objects.get(username=request.user).id
        pt.formfields = fieldJson
        pt.creation_date = timezone.now()

        if request.POST.get("isComplaint", "") == "0":
            pt.complaint = True
        else:
            pt.complaint = False

        pt.save()
        # user created community action for activity stream
        create_action(request.user, 'created a new post type:', pt)
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
    post_type = get_object_or_404(PostType, pk=id)
    communityDetail = get_object_or_404(Community, id=post_type.community_id_id)
    if post_type.formfields:
        print("minaaaaaaaa")
        print(post_type.formfields)
        form_fields = json.loads(post_type.formfields)
    else:
        form_fields = []
    context = {'post_type': post_type, 'communityDetail': communityDetail, "form_fields" : form_fields}

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

def archivePostType(request, id):
    pt = get_object_or_404(PostType, pk=id)
    pt.active = False
    pt.save()
    context = {'post_type': pt}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return HttpResponseRedirect(reverse('community:post_types', args=(pt.community_id_id, True,)))

def getCommunityStatistics(request, id):
    post_types = []
    post_counts = []
    posts = []
    comments = []

    recent_posts = []
    recent_post_types = []
    recent_commented_posts = []

    post_distributions_count = []
    post_distributions = ['Archived', 'Reported', 'Active']

    post_distributions_count.append(Post.objects.filter(community_id=id).filter(active=False).count())
    post_distributions_count.append(Post.objects.filter(community_id=id).filter(inappropriate=True).count())
    post_distributions_count.append(Post.objects.filter(community_id=id).filter(active=True).count())

    user_activities = ['Created Post', 'Created Post Type', 'Commented', 'Reported']
    user_activities_count = []

    user_activities_count.append(Post.objects.filter(community_id=id).values('user_id').distinct().count()) # created post
    user_activities_count.append(PostType.objects.filter(community_id=id).values('owner').distinct().count()) # created post type
    user_activities_count.append(Comments.objects.filter(post_id__in=(Post.objects.filter(community_id=id))).values('user_id').distinct().count()) # commented
    user_activities_count.append(InappropriatePosts.objects.filter(post_id__in=(Post.objects.filter(community_id=id))).values('user_id').distinct().count()) # reported

    post_queryset = Post.objects.filter(community_id=id).filter(creation_date__range=[timezone.now() - timedelta(days=30), timezone.now()])
    posttype_queryset = PostType.objects.filter(community_id=id).filter(creation_date__range=[timezone.now() - timedelta(days=30), timezone.now()])
    recent_comments = Comments.objects.filter(creation_date__range=[timezone.now() - timedelta(days=30), timezone.now()])
    commented_posts_queryset = Post.objects.filter(id__in=recent_comments).filter(community_id=id)

    recent_posts = list(post_queryset)
    recent_post_types = list(posttype_queryset)
    recent_commented_posts = list(commented_posts_queryset)

    for postType in PostType.objects.filter(community_id=id):
        post_count = Post.objects.filter(posttype_id=postType.pk).count()    

        post_counts.append(post_count)
        post_types.append(postType.name)

    for post in Post.objects.filter(community_id=id):
        comment_count = Comments.objects.filter(post_id=post.pk).count()
        
        posts.append(post.name)
        comments.append(comment_count)    

    context = {
                'post_types'         : post_types,
                'post_counts'        : post_counts,
                'posts'              : posts,
                'comments'           : comments,
                'recent_posts'       : recent_posts,
                'recent_posttypes'   : recent_post_types,
                'recent_comments'    : recent_commented_posts,
                'post_distributions' : post_distributions,
                'post_dist_count'    : post_distributions_count,
                'user_activities'    : user_activities,
                'user_act_count'     : user_activities_count
             }

    return render(request, "CommunityStatistics.html", context)


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
    description = description[0: 199]
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
                fieldtype  = value["fieldtype"]
                enumvals   = value["enumvals"]
                isRequired = value["isRequired"]

                if fieldtype == "LO":
                    lat = request.POST.getlist('latitude', "")
                    lon = request.POST.getlist('longitude', "")
                    
                    geolocation = {}
                    
                    for i in range(len(lat)):
                        point = {}
                        point["lat"] = lat[i]
                        point["lon"] = lon[i]

                        geolocation[i] = point

                    fieldValue = geolocation

                elif fieldtype in ["IM", "VI", "AU"]:
                    if bool(request.FILES.get(fieldlabel, False)) == True:
                        file = request.FILES[fieldlabel]
                        save_file = default_storage.save(file.name, file)
                        fieldValue = file.name
                    else:
                        fieldValue = ""
                else:
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

                json_response[fieldposnr] = json_element


    if "wiki_tag" in request.POST:
        wiki_tags["tags"] = []
        tags = request.POST.getlist('wiki_tag', "")
        for i in range(len(tags)):
            wiki_tags["tags"].append(json.loads(tags[i].replace("\'", "\"")))
       
    if name == "" or description == "":
        return HttpResponseRedirect(reverse('community:new_post', args=(id,)))

    if "cancel" in request.POST:
        return HttpResponseRedirect(reverse('community:home'))
    else:
        post = Post(name=name, description=description, user_id=User.objects.get(username=request.user),
                    creation_date=timezone.now(), community_id=community,
                    form_fields=json.dumps(json_response), posttype_id=post_type, complaint=is_complaint,
                    complaint_status=complaint_status, tags=wiki_tags)

        post.save()

        # user created post action for activity stream
        create_action(request.user, 'created a new post:', post)

        return HttpResponseRedirect(reverse('community:post_detail', args=(post.id,)))


def getPosts(request, id):
    communityPosts = Post.objects.filter(community_id=id)
    posts = []

    for post in communityPosts:
        report_count = InappropriatePosts.objects.filter(post_id=post).count()

        if report_count >= 5:
            posts.append(post)
            post.inappropriate = 1
            post.save()

    context = {'communityPosts': communityPosts}

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user

    return render(request, "PostList.html", context)


def getPostDetail(request, id):
    post = get_object_or_404(Post, pk=id)
    post_type = post.posttype_id
    comments = Comments.objects.filter(post_id=id)

    if post.form_fields:
        form_fields = json.loads(post.form_fields)

        for key, value in form_fields.items():    
            if value["fieldtype"] in ["IM", "VI", "AU"]:
                file_name = value["fieldValue"]
                if file_name:
                    file_path = default_storage.url(file_name)
                    value["fieldValue"] = file_path
    else:
        form_fields = []

    context = {'post': post, 'post_type': post_type, 'form_fields': form_fields, 'comments':comments}
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user

    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user

    return render(request, "PostDetail.html", context)


def create_comment(request, id):
    post = get_object_or_404(Post, pk=id)
    commentbox = str(request.POST.get('commentbox', "")).strip()
    
    if commentbox:
        comment = Comments(comment_body=commentbox, post_id=post, user_id=User.objects.get(username=request.user), creation_date=timezone.now())
        comment.save()

    return HttpResponseRedirect(reverse('community:post_detail', args=(post.id,)))


def report_post(request, id):
    post = get_object_or_404(Post, pk=id)
    
    inappropriatePosts = InappropriatePosts(inappropriate=True, post_id=post, user_id=User.objects.get(username=request.user))
    inappropriatePosts.save()

    return HttpResponseRedirect(reverse('community:post_detail', args=(post.id,)))


def archive_post(request, id):
    post = get_object_or_404(Post, pk=id)
    community = post.community_id
    post.active = False
    post.save()

    return HttpResponseRedirect(reverse('community:community_detail', args=(community.id,)))



def unarchive_post(request, id):
    post = get_object_or_404(Post, pk=id)
    community = post.community_id
    post.active = True
    post.save()

    return HttpResponseRedirect(reverse('community:community_detail', args=(community.id,)))


def post_list(request):
    post_list = Post.objects.order_by('-creation_date')[:30]
    context = {'post_list': post_list}
    
    if request.user.is_authenticated:
        user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = user
    
    return render(request, 'Posts.html', context)

def advanced_search(request, id):
    post_type = get_object_or_404(PostType, pk=id)

    if post_type.formfields:
        form_fields = json.loads(post_type.formfields)
    else:
        form_fields = []
    context = {'post_type': post_type, 'form_fields' : form_fields }
    if request.user.is_authenticated:
        community_user = get_object_or_404(UserAdditionalInfo, user=request.user)
        context["user"] = community_user
    return render(request, 'AdvancedSearch.html', context )



def getPostsOfPostType(request):
    pt_id = request.GET.get("pt_id", "")
    posts = list(Post.objects.filter(posttype_id_id=pt_id).values())
    print("=================")
    print(posts)
    response = { "posts": posts }
    return JsonResponse(response, safe=False)

# def search(request, id):
#     post_type = get_object_or_404(PostType, pk=id)
#     name1 = str(request.POST.get('name1', "")).strip()
#     name2 = str(request.POST.get('name2', "")).strip()
#     description1 = str(request.POST.get('description1', "")).strip()
#     description2 = str(request.POST.get('description2', "")).strip()
#     form_fields = json.loads(post_type.formfields)
#     for (k, v) in form_fields.items():
#         for (key, value) in v.items():
#             fieldlabel = value["fieldlabel"]
#             fieldtype = value["fieldtype"]
#             if fieldtype not in ["IM", "VI", "AU", "LO"]:
#                 fieldValue = str(request.POST.get(value["fieldlabel"], "")).strip()
#             else:
#                 fieldValue = str(request.POST.get(value["fieldlabel"], "")).strip()



