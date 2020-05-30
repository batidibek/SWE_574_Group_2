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
    path('posts/', community.community_list, name='post_list'),
    path('communities/<id>', community.getCommunity, name="community_detail"),
    path('communities/new-post-type/<id>', community.getCommunityHeader, name="new_post_type"),

    path('communities/post_types/<id>/<activeStatus>', community.getPostTypes, name="post_types"),
    path('communities/post_type/<id>/<activeStatus>', community.getPostType, name="post_type"),
    path('communities/post_types/detail/<id>/createpost', community.getPostType, name="new_post"),
    path('communities/new_post/<id>', community.new_post, name="new_post"),
    path('communities/posts/<id>', community.getPosts, name="posts"),
    path('communities/posts/post_detail/<id>', community.getPostDetail, name="post_detail"),
    path('communities/advanced_search/<id>', community.advanced_search, name="advanced_search"),

    path('user_profile/<id>', users.user_profile, name='user_profile'),
    path('user_profile/<id>/posts/', users.user_posts, name='user_posts'),
    path('user_profile/<id>/communities/', users.user_communities, name='user_communities'),
    path('user_profile/<id>/follows/', users.user_list, name='user_follows'),
    path('user_profile/<id>/followed/', users.user_list, name='user_followers'),
    path('user_profile/<id>/follow/', users.user_follow, name='user_follow'),

    # REQUESTS
    path('create-user/', users.create_user, name='create_user'),
    path('authenticate-user/', users.authenticate_user, name='authenticate_user'),
    path('log-out/', users.log_out, name='log_out'),
    path('create-community/', community.create_community, name='create_community'),
    path('create-post-type', community.newPostType, name="create_post_type"),
    path('getCommunityByFilter', community.getCommunityByFilter),
    path('archive_community/<id>', community.archiveCommunity, name='archive_community' ),
    path('archive_posttype/<id>', community.archivePostType, name='archive_posttype' ),
    path('create-post/<id>', community.create_post, name='create_post'),
    path('create-comment/<id>', community.create_comment, name='create_comment'),
    path('report-post/<id>', community.report_post, name='report_post'),
    path('archive-post/<id>', community.archive_post, name='archive_post'),
]
