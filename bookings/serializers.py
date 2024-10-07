from .models import *
from rest_framework import serializers

class Booking_serializer(serializers.ModelSerializer):
    class Meta:
        models = Booking
        fields = "__all__"
        