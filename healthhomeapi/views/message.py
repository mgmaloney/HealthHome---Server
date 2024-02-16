from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User

class MessageView(ViewSet):
    def create(self, request):
        try:
            sender = User.objects.get(request.data['senderId'])
            receiver = User.objects.get(request.data['receiverId'])
            message = Message.objects.create(
                content = request.data['content'],
                sender=sender,
                receiver=receiver
            )
            serializer = Message_Serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response('unable to create message', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(methods=['get'], detail=False)
    def user_messages(self, request):
        try:
            user = User.objects.get(id=request.data['userId'])
            messages = Message.objects.filter(Q(sender=user) | Q(receiver=False))
            serializer = Message_Serializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return ([], status.HTTP_200_OK)

class Message_User_Serializer:
    class Meta:
        model: User
        fields = ('first_name', 'last_name')

class Message_Serializer(serializers.ModelSerializer):
    sender = Message_User_Serializer()
    receiver = Message_User_Serializer()
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'datetime')