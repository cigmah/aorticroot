from choices.models import Choice
from choices.serializers import ChoiceSerializer
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ChoiceList(generics.ListCreateAPIView):
    """
    List all choices, or create a new choice.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('content', 'category')
    filter_fields = ('category',)

class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a choice.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
