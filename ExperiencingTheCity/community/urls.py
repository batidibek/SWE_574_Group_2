from django.urls import path
from .views import home, users


app_name = 'community'
urlpatterns = [

    #PAGES
    path('', home.homepage, name='home'),
    path('sign-up/', users.sign_up, name='sign_up'),
    path('sign-in/', users.sign_in, name='sign_in'),

    #REQUESTS
    path('create-user/', users.create_user, name='create_user'),
    path('authenticate-user/', users.authenticate_user, name='authenticate_user'),
    path('log-out/', users.log_out, name='log_out'),
]
