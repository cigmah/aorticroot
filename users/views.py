from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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

        username = request.data.get("username")
        email = request.data.get("email")

        password = User.objects.make_random_password()

        user = User.objects.create_user(username, email, password=password)

        token = Token.objects.create(user=user)

        data = {"username": user.username, "token": token.key, "password": password}

        return Response(data, status=status.HTTP_201_CREATED)


class UserStatistic(generics.RetrieveAPIView):
    """
    Gets user statistics.
    """

    pass
