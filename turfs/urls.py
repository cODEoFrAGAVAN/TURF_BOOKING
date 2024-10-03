from django.urls import path
from .views import *


urlpatterns = [
    path("checking", checking),
    path("turf_registration", turf_registration),
    path("forget_password", forget_password),
    path("check_otp", check_otp),
    path("update_password", update_password),
    path("update_turf_details", update_turf_deatils),
    path("update_turf_mobile_number", update_turf_mobile_number),
    path("verify_updated_number",verify_new_turf_mbnum)
]
