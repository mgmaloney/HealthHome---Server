from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from healthhomeapi.models import Message, User

class PatientView(ViewSet):
    def list(self, request):
        try: 
            patients = User.objects.filter(Q(provider=False) & Q(admin=False))
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response([], status=status.HTTP_200_OK)
    
    @action(methods=['get', 'put'], detail=False) 
    def get_single_patient(self, request):
        try:
            patient = User.objects.get(id=request.data['patient_id'])
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        # try:
            patient = User.objects.create(
                first_name = request.data['first_name'],
                last_name = request.data['last_name'],
                email = request.data['email'],
                phone_number = request.data['phone_number'],
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
    
    # @action(methods=['put'], detail=False)
    def update(self, request, pk):
        patient = User.objects.get(id=request.data['patient_id'])
        
        patient.first_name = request.data['first_name']
        patient.last_name = request.data['last_name']
        patient.email = request.data['email']
        patient.phone_number = request.data['phone_number']
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