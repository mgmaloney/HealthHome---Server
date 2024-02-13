from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=2000, default='')
    datetime = models.DateTimeField(auto_now_add=True)