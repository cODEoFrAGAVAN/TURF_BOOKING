from django.db import models

class User_reviews(models.Model):
    turf_ids = models.CharField(max_length=30, null=False)
    user_name = models.CharField(max_length=20,null=False,unique=True)
    review_message = models.CharField(max_length=1000,null=True)
    review_starts = models.CharField(max_length=1,null=False,default="1")
    def __str__(self):
        return self.turf_ids
    
