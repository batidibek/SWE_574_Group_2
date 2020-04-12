from django.urls import path
from .views import home, users


app_name = 'community'
urlpatterns = [

    #PAGES
    path('', home.homepage, name='home'),
    path('sign-up/', users.sign_up, name='sign_up'),

    #REQUESTS
    path('create-user/', users.create_user, name='create_user'),
]
