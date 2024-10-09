from .models import *
from rest_framework import serializers

class Booking_serializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class Store_order_id_serializer(serializers.ModelSerializer):
    class Meta:
        model = Store_order_id
        fields = '__all__'