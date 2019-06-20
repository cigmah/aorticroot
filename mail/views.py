from rest_framework import generics
from mail.models import *
from mail.serializers import *


class MailCreate(generics.CreateAPIView):
    """
    Create a new mail.
    """

    serializer_class = MailSerializer
