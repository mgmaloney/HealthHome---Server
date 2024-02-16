from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=50, default=None, null=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=15, default='')
    birthdate = models.CharField(max_length=15, default='')
    ssn = models.CharField(max_length=9, default='')
    admin = models.BooleanField()
    provider = models.BooleanField()    