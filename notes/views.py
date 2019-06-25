from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from notes.serializers import *
from notes.models import *
from questions.models import *


class NoteList(generics.ListAPIView):
    """
    List or create notes.
    
    TODO Deprecate create, should be internal only.
    """

    queryset = Note.objects \
                   .all() \
                   .order_by("year_level", "specialty")

    serializer_class = NoteListSerializer

    search_fields = (
        "title",
        "content"
    )

    filter_fields = (
        "contributor",
        "year_level",
        "specialty",
    )

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def list(self, request, *args, **kwargs):

        user = request.user

        # TODO more idiomatic or efficient ways to do this.
        if user.is_authenticated:
            notes = Note.objects.annotate(
                num_questions=Count('note_question'),
                num_comments=Count('note_comment'),
                num_due=Count(
                    'note_question__question_response',
                    filter=Q(note_question__question_response__next_due_datetime__lte=timezone.now())
                ),
                num_known=Count(
                    'note_question__question_response',
                    filter=Q(note_question__question_response__next_due_datetime__gt=timezone.now())
                ),
            )
        else:
            notes = Note.objects.annotate(
                num_questions=Count('note_question'),
                num_comments=Count('note_comment'),
            )

        serialized = NoteListSerializer(notes, many=True)

        return Response(serialized.data, status.HTTP_200_OK)

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

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class NoteCommentCreate(generics.CreateAPIView):
    """
    Create comments on notes.
    """

    serializer_class = NoteCommentSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )
