from rest_framework import generics
from rest_framework import permissions
from notes.serializers import *
from notes.models import *


class NoteListCreate(generics.ListCreateAPIView):
    """
    List or create notes.
    
    TODO Deprecate create, should be internal only.
    """

    queryset = Note.objects.all().order_by("-created_at")

    serializer_class = NoteSerializer

    search_fields = ("title", "content")

    filter_fields = ("contributor", "year_level", "specialty", "domain")

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or destroy a specific note.
    
    TODO Add missing fields.

    Response: {
        id: int,
        title: str,
        content: str,
        year_level: str,
        specialty: str,
        due: List(int),
        known: None if not auth else List(int),
        comments: List(Comment),
        created_at: str(timestamp),
        modified_at: str(timestamp),
    }
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
