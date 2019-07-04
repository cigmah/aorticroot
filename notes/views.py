from django.db.models import Count, Q, F, Max
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

    queryset = Note.objects.all()

    serializer_class = NoteListSerializer

    search_fields = (
        "title",
        "content"
    )

    filter_fields = (
        "specialty",
        "topic",
    )

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):

        specialty_filter = self.request.GET.get("specialty")
        topic_filter = self.request.GET.get("topic")
        search_filter = self.request.GET.get("search")

        queryset = self.queryset

        filters = {}
        
        if specialty_filter is not None:
            filters["specialty"] = int(specialty_filter)
        if topic_filter is not None:
            filters["topic"] = int(topic_filter)

        queryset = queryset.filter(**filters)

        if search_filter is not None:
            queryset = queryset.filter(
                Q(title__icontains=search_filter) |
                Q(content__icontains=search_filter)
            )

        return queryset

    def list(self, request, *args, **kwargs):

        user = request.user

        note_objects = self.get_queryset()

        # TODO more idiomatic or efficient ways to do this.
        if user.is_authenticated:
            notes = note_objects.annotate(
                num_due=Count(
                    'note_question__question_response__question',
                    filter=(
                        Q(note_question__question_response__next_due_datetime__lte=timezone.now()) &
                        Q(note_question__question_response__user=user) &
                        ~Q(note_question__question_response__next_due_datetime__gt=timezone.now())
                    ),
                    distinct=True,

                ),
                num_known=Count(
                    'note_question__question_response__question',
                    filter=(
                        Q(note_question__question_response__next_due_datetime__gt=timezone.now()) &
                        Q(note_question__question_response__user=user)
                    ),
                    distinct=True,

                ),
            ).order_by('specialty', 'topic')
        else:
            notes = note_objects.annotate().order_by('specialty', 'topic')

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

        all_ids = questions.filter(note=note).values('id')

        if user.is_authenticated:

            past_most_recent_responses = QuestionResponse.objects.filter(
                question__note=note,
                user=user,
            ).values(
                'question',
            ).annotate(
                most_recent=Max('next_due_datetime')
            )

            due_ids = questions.filter(
                question_response__next_due_datetime__in=[response.get("most_recent") for response in past_most_recent_responses],
                question_response__next_due_datetime__lte=timezone.now(),
            ).values('id').distinct()

            known_ids = questions.filter(
                question_response__next_due_datetime__in=[response.get("most_recent") for response in past_most_recent_responses],
                question_response__next_due_datetime__gt=timezone.now(),
            ).values('id').distinct()

            data = {
                "all_ids": all_ids,
                "due_ids": due_ids,
                'known_ids': known_ids,
                **note_serialized.data
            }

        else:

             data = {
                "all_ids": all_ids,
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
