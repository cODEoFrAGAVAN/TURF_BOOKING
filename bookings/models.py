from django.db import models

class Booking(models.Model):
    booking_id = models.CharField(max_length=20,null=False,unique=True)
    turf_id = models.CharField(max_length=20,null=False)
    booking_date_time = models.DateField(null=False)
    slot_start_date_time = models.DateField(null=False)
    slot_end_date_time = models.DateField(null=False)
    user_id = models.CharField(max_length=20,null=False)
    user_mobile_number = models.CharField(max_length=10,null=False)
    amount = models.CharField(max_length=10,null=False)
    payment_status = models.CharField(max_length=20,null=False,default='pending')
    temp_lock = models.CharField(max_length=10,default="LOCKED")
    def __str__(self) -> str:
        return self.Booking_id
    




