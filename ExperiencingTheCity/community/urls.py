from django.urls import path
from .views import home, users, community


app_name = 'community'
urlpatterns = [

    #PAGES
    path('', home.homepage, name='home'),
    path('sign-up/', users.sign_up, name='sign_up'),
    path('sign-in/', users.sign_in, name='sign_in'),
    path('new-community/', community.new_community, name='new_community'),
    path('communities/', community.community_list, name='community_list'),

    #REQUESTS
    path('create-user/', users.create_user, name='create_user'),
    path('authenticate-user/', users.authenticate_user, name='authenticate_user'),
    path('log-out/', users.log_out, name='log_out'),
    path('create-community/', community.create_community, name='create_community'),
]
