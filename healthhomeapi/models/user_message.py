from django.db import models
from .user import User
from .message import Message

class User_Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL)