from django.db import models

class PatientMed(models.Model):
  name = models.CharField(max_length=1000, default='')
  route = models.CharField(max_length=200, default='')
  dose = models.CharField(max_length=200, default='')