from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import CheckConstraint


class Test_credentials(models.Model):
    key_id = models.CharField(max_length=100,null=False)
    secret = models.CharField(max_length=100,null=False)
    saved_date_time = models.DateTimeField(default=timezone.now,null=False)
    saved_by = models.CharField(max_length=20,null=False)
    active_status = models.CharField(max_length=3,default="YES",null=False)
    class Meta:
        constraints = [
            CheckConstraint(check=Q(saved_by="ADMIN"), name='saved_by_check1'),
        ]
    def __str__(self):
        self.key_id
    
