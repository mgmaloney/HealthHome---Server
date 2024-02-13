from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=15, default='')
    birthdate = models.CharField(max_length=15, default='')
    ssn = models.IntegerField(max_digits=9, default=0)
    admin = models.BooleanField()
    provider = models.BooleanField()    