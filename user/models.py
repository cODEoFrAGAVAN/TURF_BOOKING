from django.db import models


class Login(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.user_name
    
