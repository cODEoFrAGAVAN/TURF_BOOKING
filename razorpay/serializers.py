from .models import *
from rest_framework import serializers

class Test_credentials_serializers(serializers.ModelSerializer):
    class Meta:
        model = Test_credentials
        fields = '__all__'