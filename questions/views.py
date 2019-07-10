from django.core.exceptions import ObjectDoesNotExist
from random import choice, sample
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

    queryset = Question.objects \
                       .all() \
                       .order_by("id")

    serializer_class = QuestionSerializer

    search_fields = (
        "stem",
        "note__title",
        "note__content"
    )

    filter_fields = (
        "note",
        "note__contributor",
        "domain",
        "year_level",
        "note__specialty",
        "note__topic",
        "contributor",
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
        note_id = request.data.get("note_id")
        domain = request.data.get("domain")
        stem = request.data.get("stem")
        choices = request.data.get("choices")
        year_level = request.data.get("year_level")
        domain = request.data.get("domain")

        if None in [note_id, domain, stem, choices]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Get the note out of the request
        # TODO more idiomatic way to do this
        note = Note.objects.get(id=note_id)

        try:
            # Assert only one correct choice
            correct = [choice for choice in choices if choice["is_correct"]]
            assert len(correct) == 1

            # Assert there is at least one other option
            assert len(choices) - len(correct) > 0

            # Assert that the stem is not blank
            assert stem.strip() != ""

            # Assert that choices are not blank
            choice_blank = [choice.get("content").strip() == "" for choice in choices]
            assert not any(choice_blank)

            # Assert that choices are unique
            choices_content = [choice.get("content").strip() for choice in choices]
            choices_set = set(choices_content)
            assert len(choices_content) == len(choices_set)

        except AssertionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Add the question
        question = Question.objects.create(
            contributor=contributor,
            note=note,
            stem=stem,
            year_level=year_level,
            domain=domain,
        )

        # TODO Find a way to do this in bulk.
        # bulk_create() had issues.
        for choice in choices:
            QuestionChoice.objects.create(
                question=question,
                **choice
            )

        serialized = QuestionSerializer(question)

        return Response(
            serialized.data,
            status=status.HTTP_201_CREATED
        )


class QuestionRandom(generics.RetrieveAPIView):
    """
    Retrieves a single random question.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_fields = (
        "note",
        "note__contributor",
        "note__topic",
        "note__specialty",
        "year_level",
        "domain",
        "contributor",
    )

    def retrieve(self, request, *args, **kwargs):
        """
        Takes a query parameter quantity.
        TODO if user is authenticated, mix with spaced repetition
        """

        queryset = super().get_queryset()

        question_ids = list(
            self.filter_queryset(
                self.get_queryset()
            ).values_list("id", flat=True)
        )

        if len(question_ids) > 0:

            random_id = choice(question_ids)

            question = Question.objects.get(id=random_id)

            serialized = QuestionSerializer(question)

            return Response(
                serialized.data,
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_404_NOT_FOUND)

class QuestionRandomList(generics.RetrieveAPIView):
    """
    Retrieves a list of random question IDs.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_fields = (
        "note",
        "note__contributor",
        "year_level",
        "domain",
        "note__topic",
        "note__specialty",
        "contributor",
    )

    def retrieve(self, request, *args, **kwargs):
        """
        Takes a query parameter quantity.
        TODO if user is authenticated, mix with spaced repetition
        """

        queryset = super().get_queryset()

        question_ids = list(
            self.filter_queryset(
                self.get_queryset()
            ).values_list("id", flat=True)
        )

        quantity_string = self.request.GET.get("quantity")

        if quantity_string is not None:
            quantity = int(quantity_string)
        else:
            quantity = 10 # default to 10 random questions

        selected_ids = sample(question_ids, min(quantity, len(question_ids)))


        return Response(selected_ids, status=status.HTTP_200_OK)


class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a question.

    """

    queryset = Question.objects.all()

    serializer_class = QuestionSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def retrieve(self, request, *args, **kwargs):

        user = request.user

        question_id = kwargs.get('pk')

        if question_id is None:
            return Response(status.HTTP_404_NOT_FOUND)

        try:
            question = Question.objects.filter(id=question_id).get()
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        question_serialized = QuestionSerializer(question)

        if user.is_authenticated:

            liked = QuestionLike.objects.filter(
                question=question,
                user=user
            ).exists()

            num_seen = QuestionResponse.objects.filter(
                question=question,
                user=user
            ).count()

            data = {
                **question_serialized.data,
                'liked': liked,
                'num_seen': num_seen,
            }

        else:

            data = {
                **question_serialized.data
            }

        return Response(data, status=status.HTTP_200_OK)


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

class QuestionCommentCreate(generics.CreateAPIView):
    """
    Create comments on questions.
    """

    serializer_class = QuestionCommentSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )

class QuestionResponseList(generics.ListAPIView):
    """
    Returns a paginated list of question responses.
    """


    queryset = QuestionResponse.objects.all()

    serializer_class = QuestionResponseListSerializer

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user).order_by('-created_at')
        return queryset
