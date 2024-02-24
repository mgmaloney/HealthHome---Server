from django.db import models
from .user import User
from .conversation import Conversation

class Message(models.Model):
    content = models.CharField(max_length=2000, default='')
    datetime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='message_sender')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='message_receiver')
    read= models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, related_name='conversation_messages', on_delete=models.SET_NULL, null=True, default=None)