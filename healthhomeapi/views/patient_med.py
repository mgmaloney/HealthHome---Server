from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from rest_framework.decorators import action
from healthhomeapi.models import PatientMed, User

class PatientMedView(ViewSet):
  def retrieve(self, request, pk):
    patient_med = PatientMed.objects.get(pk=pk)
    serializer = PatientMedSerializer(patient_med)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @action(methods=['get', 'put'], detail=False)
  def get_all_patient_meds(self, request):
    patient = User.objects.get(id=request.data['patient_id'])
    patient_medications = PatientMed.objects.filter(patient=patient)
    serializer = PatientMedSerializer(patient_medications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    patient = User.objects.get(id=request.data['patient_id'])
    patient_med = PatientMed.objects.create(
      patient = patient,
      name = request.data['name'],
      route = request.data['route'],
      dose = request.data['dose']
    )
    serializer = PatientMedSerializer(patient_med)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    patient_med = PatientMed.objects.get(pk=pk)
    patient_med.name = request.data['name']
    patient_med.route = request.data['route']
    patient_med.dose = request.data['dose']
    patient_med.save()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def destroy(self, request, pk):
    patient_med = PatientMed.objects.get(pk=pk)
    patient_med.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class PatientMedSerializer(serializers.ModelSerializer):
  class Meta:
    model = PatientMed
    fields = ('id', 'name', 'route', 'dose')