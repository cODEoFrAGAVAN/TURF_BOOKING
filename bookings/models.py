from django.utils import timezone
from django.db import models

class Booking(models.Model):
    booking_id = models.CharField(max_length=20,null=False,unique=True)
    turf_id = models.CharField(max_length=20,null=False)
    booking_date_time = models.DateTimeField(null=False,default=timezone.now)
    slot_start_date_time = models.DateTimeField(null=False,default=timezone.now)
    slot_end_date_time = models.DateTimeField(null=False,default=timezone.now)
    user_id = models.CharField(max_length=20,null=False)
    user_mobile_number = models.CharField(max_length=10,null=False)
    amount = models.CharField(max_length=10,null=False)
    payment_status = models.CharField(max_length=20,null=False,default="PENDING")
    temp_lock = models.CharField(max_length=10,default="LOCKED")
    def __str__(self) -> str:
        return self.Booking_id
    
class Store_order_id(models.Model):
    booking_id = models.CharField(max_length=20,null=False,unique=True)
    payment_id = models.CharField(max_length=20,null=False)
    payment_status = models.CharField(max_length=20,null=False,default='PENDING')



