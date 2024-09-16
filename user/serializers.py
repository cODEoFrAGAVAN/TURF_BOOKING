from rest_framework import serializers
from .models import *

class Login_serializer1(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'



class User_Signup_serializer1(serializers.ModelSerializer):
    class Meta:
        model = User_signup
        fields = '__all__'


class Random_token_seriallizer1(serializers.ModelSerializer):
    class Meta:
        model = Random_token_generation
        fields = '__all__'
    

class Forget_user_password_serializer1(serializers.ModelSerializer):
    class Meta:
        model = Forget_user_password
        fields = ['user_name','mobile_number','mailid','otp']
