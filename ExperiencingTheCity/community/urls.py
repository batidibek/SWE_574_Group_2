from django.urls import path
from .views import home, users, community

app_name = 'community'
urlpatterns = [

    # PAGES
    path('', home.homepage, name='home'),
    path('sign-up/', users.sign_up, name='sign_up'),
    path('sign-in/', users.sign_in, name='sign_in'),
    path('new-community/', community.new_community, name='new_community'),
    path('communities/', community.community_list, name='community_list'),
    path('communities/<id>', community.getCommunity, name="community_detail"),
    path('communities/new-post-type/<id>', community.getCommunityHeader, name="new_post_type"),
    path('communities/post_types/<id>', community.getPostTypes, name="post_types"),
    path('communities/post_types/detail/<id>', community.getPostType, name="post_type"),
    path('communities/post_types/detail/<id>/createpost', community.getPostType, name="post_type"),

    # REQUESTS
    path('create-user/', users.create_user, name='create_user'),
    path('authenticate-user/', users.authenticate_user, name='authenticate_user'),
    path('log-out/', users.log_out, name='log_out'),
    path('create-community/', community.create_community, name='create_community'),
    path('create-post-type', community.newPostType, name="create_post_type"),

    # TEMPORARY
    path('UserActivityStream', users.activity_stream, name='activity_stream'),
]
