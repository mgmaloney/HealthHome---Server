from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User

class UserView(ViewSet):
    def retrieve(self, request):
        try:
            user = User.objects.get(id=request.data['userId'])
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        try:
            user = User.objects.create(
                first_name = request.data['firstName'],
                last_name = request.data['lastName'],
                email = request.data['email'],
                phone_number = request.data['phoneNumber'],
                address = request.data['address'],
                birthdate = request.data['birthdate'],
                ssn = request.data['ssn'],
                admin = request.data['admin'],
                provider = request.data['provider']
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'unable to create user'})

class UserSerializer(serializers.ModelSerializer):
    ssn = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthdate', 'email', 'phone_number', 'address' 'ssn')
    def get_ssn(self, obj):
        return obj.ssn[:-4]