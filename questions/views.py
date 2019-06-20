from random import sample
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from questions.models import *
from questions.serializers import *

class QuestionListCreate(generics.ListCreateAPIView):
    """
    List all questions, or create a new question.
    """

    queryset = Question \
        .objects \
        .all() \
        .order_by('id')

    serializer_class = QuestionSerializer

    search_fields = (
        'stem',
        'note__title',
        'note__content',
    )

    filter_fields = (
        'note',
        'note__contributor',
        'note__year_level',
        'note__specialty',
        'note__domain',
        'contributor',
    )

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def create(self, request, *args, **kwargs):
        """
        On creation:
        1. Get the user from the request.
        2. Ensure there is exactly one correct choice given.
        """
        # TODO Would prefer to eventually move to serializers.

        # Get the user from the request
        contributor = request.user
        note_id = request.data.get('note_id')
        stem = request.data.get('stem')
        choices = request.data.get('choices')

        if None in [note_id, stem, choices]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Get the note out of the request
        # TODO more idiomatic way to do this
        note = Note.objects.get(id=note_id)

        # Assert only one correct choice
        correct = [choice for choice in choices if choice['is_correct']]
        assert len(correct) == 1

        # Assert there is at least one other option
        assert len(choices) - len(correct) > 0

        # Add the question
        question = Question.objects.create(
            contributor=contributor,
            note=note,
            stem=stem,
        )

        # TODO Find a way to do this in bulk.
        # bulk_create() had issues.
        for choice in choices:
            QuestionChoice.objects.create(
                question=question,
                **choice
            )

        data = {
            'id': question.id,
        }

        return Response(data, status=status.HTTP_201_CREATED)

class QuestionRandomList(generics.RetrieveAPIView):
    """
    Retrieves a list of random question IDs.
    """

    def retrieve(self, request, *args, **kwargs):
        """
        Takes a query parameter quantity.
        TODO if user is authenticated, mix with spaced repetition
        """

        quantity = kwargs.get('quantity', 10)

        question_ids = list(
            Question \
                .objects \
                .all() \
                .values_list('id', flat=True)
        )

        selected_ids = sample(
            question_ids,
            min(quantity, len(question_ids))
        )

        data = {
            'ids': selected_ids,
        }

        return Response(data, status=status.HTTP_200_OK)

class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a question.
    """
    queryset = Question.objects.all()

    serializer_class = QuestionSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class QuestionResponseCreate(generics.CreateAPIView):

    serializer_class = QuestionResponseSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )

class QuestionLikeCreate(generics.CreateAPIView):
    """
    Creates a like on a question.
    Perhaps this should be moved to a diferent API,
    as this should be idempotent.
    """

    serializer_class = QuestionLikeSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )

class QuestionFlagCreate(generics.CreateAPIView):
    """
    Creates a flag on a question.
    Again, perhaps like QuestionLike, this should be
    moved to a different API as it should also be idempotent.
    """

    serializer_class = QuestionFlagSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )
