from .models import *
from rest_framework import serializers


class User_review_serializers(serializers.ModelSerializer):
    class Meta:
        model = User_reviews
        fields = "__all__"


# class update_review_serializers(serializers.ModelSerializer):
#     class Meta:
#         model = User_reviews
#         fields = ['turf_id','review_message']
