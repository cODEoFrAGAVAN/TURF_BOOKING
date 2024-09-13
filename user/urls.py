from .views import *
from django.urls import path

urlpatterns = [
    path('login',login),
    path('signup',user_signin_up)
]
