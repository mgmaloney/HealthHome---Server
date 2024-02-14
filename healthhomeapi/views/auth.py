from rest_framework.decorators import api_view
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from healthhomeapi.models import User

@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated User Account

    Method arguments:
      request -- The full HTTP request object
    '''
    user = User.objects.filter(uid=request.data['uid'])

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'phoneNumber': user.phone_number,
            'address': user.address,
            'birthdate': user.birthdate,
            'ssn': user.ssn[:-4],
            'admin': user.admin,
            'provider': user.provider
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def patient_first_login_check(request):
    user = User.objects.filter(first_name=request.data['firstName'], last_name=request.data['lastName'], birthdate=request.data['birthdate'], ssn__endswith=request.data['ssn'])
    if user is not None:
        user.uid = request.data['uid']

    # Return the user info to the client
        data = {
            'id': user.id,
            'uid': user.uid,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'phoneNumber': user.phone_number,
            'address': user.address,
            'birthdate': user.birthdate,
            'ssn': user.ssn[:-4],
            'admin': user.admin,
            'provider': user.provider
        }
        return Response(data, status=status.HTTP_200_OK)
    
    else:
        data = { 'valid': False }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
