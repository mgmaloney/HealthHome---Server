from django.db import models

class DBMed(models.Model):
  name = models.CharField(max_length=1000, default='')
  route = models.CharField(max_length=200, default='')