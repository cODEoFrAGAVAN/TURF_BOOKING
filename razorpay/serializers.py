from .models import *
from rest_framework import serializers

class Test_credentials_serializers(models.model):
    class Meta:
        model = Test_credentials
        fields = '__all__'