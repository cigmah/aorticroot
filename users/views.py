from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from users.serializers import *


class UserCreate(generics.CreateAPIView):
    """
    Creates a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # TODO move to serializer?
        # TODO Validate username and email

        username = request.data.get("username")
        email = request.data.get("email")

        password = User.objects.make_random_password()

        user = User.objects.create_user(username, email, password=password)

        token = Token.objects.create(user=user)

        data = {"username": user.username, "token": token.key, "password": password}

        return Response(data, status=status.HTTP_201_CREATED)

class Authenticate(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
        })

class UserStatistic(generics.RetrieveAPIView):
    """
    Gets user statistics.
    """

    pass
