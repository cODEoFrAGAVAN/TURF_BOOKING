from django.db import models
from django.utils import timezone


class Login(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.user_name


class User_signup(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10,primary_key=True)
    mailid = models.EmailField(unique=True,max_length=50)
    user_name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.user_name
    
