from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from healthhomeapi.models import Allergy, User

class AllergyView(ViewSet):
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized allergy instance"""
        patient = User.objects.get(id=request.data['patient_id'])
        allergy = Allergy.objects.create(
            name = request.data['name'],
            severity = request.data['severity'],
            reaction = request.data['reaction'],
            patient = patient
        )
        serializer = AllergySerializer(allergy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        patient = User.objects.get(id=request.data['patient_id'])
        allergy = Allergy.objects.get(pk=pk)
        allergy.name = request.data['name']
        allergy.severity = request.data['severity']
        allergy.reaction = request.data['reaction']
        allergy.patient = patient
        allergy.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        allergy = Allergy.objects.get(pk=pk)
        allergy.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get', 'put'], detail=False)
    def patient_allergies(self, request):
        # try:
            patient = User.objects.get(id=request.data['patient_id'])
            allergies = Allergy.objects.filter(patient=patient)
            serializer = AllergySerializer(allergies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # except:
        #     return Response([], status=status.HTTP_404_NOT_FOUND)
        

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ('id', 'name', 'severity', 'reaction', 'patient')