from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
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
from django.utils import timezone
from ..utils import wiki_data, annotation_client
from django.db.models import Q
from django.core.files.storage import default_storage
from ..utils.activity_stream import create_action

def annotate(request, id):
    post = get_object_or_404(Post, pk=id)
    annotation_body = str(request.POST.get('annotation_body', ""))
    selector_value = request.POST.get('selectorValue', "")
    target_source = str(request.POST.get('targetSource', ""))
    user = str(request.POST.get('user', ""))
    request_body = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "body": {
            "type": "TextualBody",
            "value": annotation_body,
            "format": "text/plain"
        },
        "target": {
            "source": target_source,
            "selector": {
                "type": "CssSelector",
                "value": selector_value
            }
        },
        "creator": user
    }
    annotation = annotation_client.new_annotation(request_body)
    print(annotation)
    return HttpResponseRedirect(reverse('community:post_detail', args=(post.id,)))