from .views import *
from django.urls import path

urlpatterns = [
    path("tcred",test_credentials),
    path("lcred",live_credentials)
]