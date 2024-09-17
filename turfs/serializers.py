from .models import *
from rest_framework import serializers

class Turf_registration_serializers(serializers.ModelSerializer):
    class Meta:
        model = Turf_registration
        fields = '__all__'

class Forget_turf_password_serializers(serializers.ModelSerializer):
    class Meta:
        model = Forget_turf_password
        fields = '__all__'

class Random_token_seriallizer1(serializers.ModelSerializer):
    class Meta:
        model = Random_token_generation
        fields = '__all__'


