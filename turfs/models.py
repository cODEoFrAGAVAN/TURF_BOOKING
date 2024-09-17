from django.db import models
from django.utils import timezone


class Turf_registration(models.Model):
    turf_name = models.CharField(max_length=50,null=False)
    turf_address = models.CharField(max_length=500,null=False)
    turf_pincode = models.CharField(max_length=6,null=False)
    turf_mobile_number = models.CharField(max_length=10,primary_key=True,null=False)
    turf_mailid = models.EmailField(max_length=50,unique=True,null=False)
    turf_land_line_number = models.CharField(max_length=20,null=True)
    turf_images_path = models.JSONField(max_length=1000,null=False)
    registration_date = models.DateField(default=timezone.now)
    user_name = models.CharField(max_length=20,unique=True,null=False)
    password = models.CharField(max_length=128,null=False)
    def __str__(self) -> str:
        return self.user_name

class Random_token_generation(models.Model):
    turf_mobile_number = models.ForeignKey(Turf_registration,on_delete=models.CASCADE,default='0000000000')
    user_name = models.CharField(max_length=20,unique=True)
    random_token = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.user_name


class Forget_turf_password(models.Model):
    user_name = models.CharField(max_length=20,null=False)
    mobile_number = models.CharField(max_length=10,primary_key=True,null=False)
    mailid = models.EmailField(max_length=50,unique=True,null=False)
    otp = models.CharField(max_length=6,null=False)
    isvalid = models.CharField(null=False,default='True',max_length=10)
    def __str__(self) -> str:
        return self.user_name
    
