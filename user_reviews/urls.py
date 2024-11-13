from django.urls import path
from .views import *

urlpatterns = [
    path("post_reviews", post_reviews),
    path("get_reviews_t", get_reviews_by_turf_id),
]
