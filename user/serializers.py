from rest_framework import serializers
from .models import *

class Login_serializer1(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'
