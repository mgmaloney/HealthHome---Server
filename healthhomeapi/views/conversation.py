from datetime import datetime, timezone
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User, Conversation

class ConversationView(ViewSet):
  @action(methods=['get', 'put'], detail=False)
  def get_conversations(self, request):
    user = User.objects.get(id=request.data['userId'])
    conversations = []
    distinct_conversations = list(Message.objects.filter(Q(sender=user) | Q(recipient=user)).values('conversation').distinct())
    current_most_recent_message = None
    current_most_recent_date = datetime(1921, 6, 1, tzinfo=timezone.utc)
    for distinct_conversation in distinct_conversations:
      conversation_messages = Message.objects.filter(conversation=distinct_conversation['conversation'])
      for message in conversation_messages:
        if message.datetime > current_most_recent_date:
          current_most_recent_date = message.datetime
          current_most_recent_message = message
      conversations.append(current_most_recent_message)
      current_most_recent_date = datetime(1921, 6, 1, tzinfo=timezone.utc)
    
    serializer = Message_Serializer(conversations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  @action(methods=['get', 'put'], detail=False)
  def get_single_conversation(self, request):
    user = User.objects.get(id=request.data['userId'])
    recipient = User.objects.get(id=request.data['recipientId'])
    messages = list(Message.objects.filter((Q(sender=user) & Q(recipient=recipient)) | (Q(sender=recipient) & Q(recipient=user))))
    if (len(messages) > 0):
      conversation = Conversation.objects.get(id=messages[0].conversation.id)
      serializer = ConversationSerializer(conversation)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response([], status=status.HTTP_200_OK)

class Message_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ('id', 'first_name', 'last_name', 'credential')

class Message_Serializer(serializers.ModelSerializer):
    sender = Message_User_Serializer()
    recipient = Message_User_Serializer()
    class Meta:
        model = Message
        fields = ('id', 'content', 'sender', 'recipient', 'datetime', 'conversation')

class ConversationSerializer(serializers.ModelSerializer):
  conversation_messages = serializers.SerializerMethodField()
  class Meta:
    model = Conversation
    fields = ('id', 'conversation_messages')
    depth = 1
  
  def get_conversation_messages(self, obj):
    messages = Message.objects.filter(conversation=obj).order_by('datetime')
    serializer = Message_Serializer(messages, many=True)
    return serializer.data