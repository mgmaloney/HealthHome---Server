from django.db import models
from .user import User
class PatientMed(models.Model):
  name = models.CharField(max_length=1000, default='')
  route = models.CharField(max_length=200, default='')
  dose = models.CharField(max_length=200, default='')
  patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patient_medications')