from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User

class PatientView(ViewSet):
    def retrieve(self, request):
        try:
            patient = User.objects.get(id=request.data['patientId'])
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        # try:
            patient = User.objects.create(
                first_name = request.data['firstName'],
                last_name = request.data['lastName'],
                email = request.data['email'],
                phone_number = request.data['phoneNumber'],
                address = request.data['address'],
                birthdate = request.data['birthdate'],
                ssn = request.data['ssn'],
                sex = request.data['sex'],
                gender = request.data['gender']
            )
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response({'message': 'unable to create patient'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk):
        patient = User.objects.get(id=request.data['patientId'])
        
        patient.first_name = request.data['firstName']
        patient.last_name = request.data['lastName']
        patient.email = request.data['email']
        patient.phone_number = request.data['phoneNumber']
        patient.address = request.data['address']
        patient.birthdate = request.data['birthdate']
        patient.ssn = request.data['ssn']
        patient.sex = request.data['sex']
        patient.gender = request.data['gender']
        
        patient.save()

        serializer = PatientSerializer(patient)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
class PatientSerializer(serializers.ModelSerializer):
    ssn = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthdate', 'sex', 'gender','email', 'phone_number', 'address', 'ssn')
    
    def get_ssn(self, obj):
        return obj.ssn[:-4]