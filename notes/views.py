from django.db.models import Count, Q, F
from django.utils import timezone
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from notes.serializers import *
from notes.models import *
from questions.models import *
from questions.serializers import QuestionIdSerializer


class NoteList(generics.ListAPIView):
    """
    List notes.
    """

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

        year_level = kwargs.get('year_level')

        if year_level is not None:
            note_objects = Note.objects.filter(year_level=year_level)
        else:
            note_objects = Note.objects

        # TODO more idiomatic or efficient ways to do this.
        if user.is_authenticated:
            notes = note_objects.annotate(
                num_questions=Count('note_question'),
                num_comments=Count('note_comment'),
                num_due=Count(
                    'note_question__question_response',
                    filter=(
                        Q(note_question__question_response__next_due_datetime__lte=timezone.now()) &
                        Q(note_question__question_response__user=user)
                    )

                ),
                num_known=Count(
                    'note_question__question_response',
                    filter=(
                        Q(note_question__question_response__next_due_datetime__gt=timezone.now()) &
                        Q(note_question__question_response__user=user)
                    )
                ),
            ).order_by('specialty')
        else:
            notes = Note.objects.annotate(
                num_questions=Count('note_question'),
                num_comments=Count('note_comment'),
            ).order_by('specialty')

        serialized = NoteListSerializer(notes, many=True)

        return Response(serialized.data, status.HTTP_200_OK)

class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or destroy a specific note.
    
    """

    queryset = Note.objects.all()

    serializer_class = NoteSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def retrieve(self, request, *args, **kwargs):
        # TODO Handle no ID

        user = request.user

        note_id = kwargs.get('pk')

        try:
            note = Note.objects.filter(id=note_id).get()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        note_serialized = NoteSerializer(note)

        # Manually annotating lists of questions for now.
        questions = Question.objects.all()

        all_ids = questions.filter(note=note)
        all_serialized = QuestionIdSerializer(all_ids, many=True)

        if user.is_authenticated:

            due_ids = questions.filter(
                note=note,
                question_response__next_due_datetime__lte=timezone.now(),
                question_response__user=user
            )
            due_serialized = QuestionIdSerializer(due_ids, many=True)

            known_ids = questions.filter(
                note=note,
                question_response__next_due_datetime__gt=timezone.now(),
                question_response__user=user
            )
            known_serialized = QuestionIdSerializer(known_ids, many=True)

            data = {
                "all_ids": all_serialized.data,
                "due_ids": due_serialized.data,
                'known_ids': known_serialized.data,
                **note_serialized.data
            }

        else:

             data = {
                "all_ids": all_serialized.data,
                **note_serialized.data
            }

        return Response(data, status=status.HTTP_200_OK)



class NoteCommentCreate(generics.CreateAPIView):
    """
    Create comments on notes.
    """

    serializer_class = NoteCommentSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )
