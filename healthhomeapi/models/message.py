from django.db import models
from .user import User

class Message(models.Model):
    content = models.CharField(max_length=2000, default='')
    datetime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL)