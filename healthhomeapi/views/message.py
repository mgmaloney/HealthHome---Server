from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User, Conversation

class MessageView(ViewSet):
    def create(self, request):
        # try:
            sender = User.objects.get(id=request.data['senderId'])
            recipient = User.objects.get(id=request.data['recipientId'])
            conversation = ''
            if 'conversationId' in request.data:
                conversation = Conversation.objects.get(id=request.data['conversationId'])
            else:
                conversation = Conversation.objects.create()
            message = Message.objects.create(
                content = request.data['content'],
                sender=sender,
                recipient=recipient,
                conversation=conversation
            )
            serializer = Message_Serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response('unable to create message', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(methods=['put'], detail=False)
    def user_messages(self, request):
        try:
            user = User.objects.get(id=request.data['userId'])
            messages = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-datetime')
            serializer = Message_Serializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return ([], status.HTTP_200_OK)
        
    
    @action(methods=['get', 'put'], detail=False)
    def unread_messages_count(self, request):
        try:
            user = User.objects.get(id=request.data['userId'])
            message_count = Message.objects.filter(Q(recipient=user) & Q(read=False)).count()
            return Response(message_count, status=status.HTTP_200_OK)
        
        except:
            return Response({'failed': 'true'}, status=status.HTTP_404_NOT_FOUND)
 
    
    @action(methods=['get', 'put'], detail=False)
    def read_message(self, request):
        try:
            message = Message.objects.get(id=request.data['messageId'])
            message.read = True
            message.save()
            return Response(None, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'failed': 'true'}, status=status.HTTP_304_NOT_MODIFIED)
    
    def destroy(self, request, pk):
        """only for development build"""
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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