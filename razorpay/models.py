from django.db import models

class Test_credentials(models.Model):
    key_id = models.CharField(max_length=100,null=False)
    secret = models.CharField(max_length=100,null=False)
    def __str__(self):
        self.key_id
    
