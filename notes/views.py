from rest_framework import generics
from rest_framework import permissions
from notes.serializers import *
from notes.models import *


class NoteListCreate(generics.ListCreateAPIView):
    """
    List or create notes.
    """

    queryset = Note.objects.all().order_by("-created_at")

    serializer_class = NoteSerializer

    search_fields = ("title", "content")

    filter_fields = ("contributor", "year_level", "specialty", "domain")

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or destroy a specific note.
    """

    queryset = Note.objects.all()

    serializer_class = NoteSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class NoteCommentCreate(generics.CreateAPIView):
    """
    Create comments on notes.
    """

    serializer_class = NoteCommentSerializer

    permission_classes = (permissions.IsAuthenticated,)
