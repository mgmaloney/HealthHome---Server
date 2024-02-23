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
    messages = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('datetime', 'conversation_id')
    
    
    serializer = ConversationSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  @action(methods=['get', 'put'], detail=False)
  def get_single_conversation(self, request):
    user = User.objects.get(id=request.data['userId'])
    recipient = User.objects.get(id=request.data['recipientId'])
    messages = list(Message.objects.filter((Q(sender=user) & Q(recipient=recipient)) | (Q(sender=recipient) & Q(recipient=user))))
    conversation = Conversation.objects.get(id=messages[0].conversation.id)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
    messages = Message.objects.filter(conversation=obj).order_by('-datetime')
    serializer = Message_Serializer(messages, many=True)
    return serializer.data