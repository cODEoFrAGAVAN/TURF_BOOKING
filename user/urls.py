from .views import *
from django.urls import path

urlpatterns = [
    path("login",login),
    path("signup",user_signin_up),
    path("forget_password",forget_user_password),
    path("verify_otp",verify_otp),
    path("update_password",update_password)
]
