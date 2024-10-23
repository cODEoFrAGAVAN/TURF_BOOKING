from .models import *
from rest_framework import serializers

class User_review_serializers(serializers.ModelSerializer):
    class Meta:
        model = User_reviews
        fields = '__all__'
        