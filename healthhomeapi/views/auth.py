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
    user = User.objects.filter(first_name=request.data['firstName'], last_name=request.data['lastName'], birthdate=request.data['birthdate'], ssn__endswith=request.data['ssn'])

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
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
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    user = User.objects.create(
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        email=request.data["email"],
        phone_number=request.data['phoneNumber'],
        address=request.data['address'],
        birthdate=request.data['birthdate'],
        ssn=request.data['ssn'],
        admin=request.data['admin'],
        provider=request.data['provider'],
    )

    # Return the user info to the client
    data = {
        'id': user.id,
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
    return Response(data, status=status.HTTP_201_CREATED)
