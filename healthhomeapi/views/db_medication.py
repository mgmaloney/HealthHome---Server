from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import status
from healthhomeapi.models import DBMed

class DBMedView(ViewSet):
  def list(self, request):
    db_meds = DBMed.objects.all()
    serializer = DBMedSerializer(db_meds, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class DBMedSerializer(serializers.ModelSerializer):
  class Meta:
    model = DBMed
    fields = ('id', 'name', 'route')