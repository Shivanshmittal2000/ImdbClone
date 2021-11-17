from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken  # for using jwt token

# these all if for use to create token when registration 
# commeting the below code as i use jwt token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        return Response(status=status.HTTP_200_OK)
# Create your views here.

@api_view(['POST',])
def logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration(request):
    if request.method == "POST":
        data={}
        serializer=RegistrationSerializer(data=request.data)  # it creates the user 
        print(serializer)
        if serializer.is_valid():
            account=User.objects.create(username=serializer.validated_data['username'],email=serializer.validated_data['email']) 
            #  We need to set password in this way for generating token through login
            account.set_password(serializer.validated_data['password'])
            account.save()
            data['Response']='Successfully Registered'
            data['username']=account.username
            data['email']=account.email
            token = Token.objects.get(user=account).key # not use in jwt token it is for token authentication
            data['token']=token
            return Response(data,status=status.HTTP_201_CREATED)
            # refresh = RefreshToken.for_user(account)
            # data['token']={
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }

            
            # return Response(serializer.data)
        else :
            data=serializer.errors
        return Response(data)

