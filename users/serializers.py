""" Serializers for Users. 
"""

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serializes a user for public view.

    Only the username and ID are included; the password is ommitted (for
    obvious reasons).

    """
    class Meta:
        model = User
        fields = ("id", "username")
