from .views import *
from django.urls import path

urlpatterns = [
    path("turf_list",show_turf_list)
]