from tags.models import Tag
from tags.serializers import TagSerializer
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class TagList(generics.ListCreateAPIView):
    """
    List all tags, or create a new tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('content', 'category')
    filter_fields = ('category',)

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
