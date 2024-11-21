from .views import *
from django.urls import path

urlpatterns = [
    path("turf_list", show_turf_list),
    path("booking", booking),
    path("verify_payment", verify_payment),
    path("vpa",via_upi_payment)
]
