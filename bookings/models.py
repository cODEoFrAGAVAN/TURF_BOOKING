from django.db import models

class Booking(models.Model):
    Booking_id = models.CharField(max_length=20,null=False,unique=True)
    turf_id = models.CharField(max_length=20,null=False)
    Booking_date_time = models.DateField(null=False)
    Slot_date_time = models.DateField(null=False)
    user_id = models.CharField(max_length=20,null=False)
    user_mobile_number = models.CharField(max_length=10,null=False)
    Amount = models.CharField(max_length=10,null=False)
    payment_status = models.CharField(max_length=20,null=False,default='pending')
    def __str__(self) -> str:
        return self.Booking_id
    




