from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserWallet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    account_no = models.CharField(max_length=5)
    balance = models.IntegerField()