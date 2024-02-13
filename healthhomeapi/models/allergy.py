from django.db import models
from .user import User

class Allergy(models.Model):
    name = models.CharField(max_length=50, default='')
    severity = models.CharField(max_length=25, default='')
    reaction = models.CharField(max_length=300, default='')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)