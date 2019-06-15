from questions.models import *
from questions.serializers import *
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from tags.models import Tag
from choices.models import Choice

class QuestionList(generics.ListCreateAPIView):
    """
    List all questions, or create a new question.
    """
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('tags', 'stem', 'answer', 'explanation')
    filter_fields = ('tags', 'user_id', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def extract_content(self, content_dict):
        content = content_dict.pop('content')
        return {
            'content': content,
            'defaults': content_dict
        }

    def create(self, request, *args, **kwargs):
        # TODO move this function to a serializer?
        data = request.data
        user = request.user

        # Pop nested data
        tag_data = data.pop('tags')
        distractor_data = data.pop('distractors')
        answer_data = data.pop('answer')

        # Get or create tags and choices
        # TODO Put into tag and choice serializer instead?
        tags = [Tag.objects.get_or_create(**self.extract_content(tag))[0] for tag in tag_data]
        distractors = [Choice.objects.get_or_create(**self.extract_content(distractor))[0] for distractor in distractor_data]
        (answer, _) = Choice.objects.get_or_create(**answer_data)

        question = Question.objects.create(answer=answer, user_id=user, **data)

        for tag in tags:
            QuestionTag.objects.create(question_id=question, tag_id=tag)

        for distractor in distractors:
            QuestionDistractor.objects.create(question_id=question, choice_id=distractor)

        serialized = QuestionSerializer(question)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionCommentList(generics.ListCreateAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentSerializer
    filter_backends = (DjangoFilterBackend)
    filter_fields = ('question_id', 'user_id', 'timestamp')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        # TODO Move to serializers?

        data = request.data

        question = Question.objects.get(id=data.get('question_id'))

        question_comment = QuestionComment.objects.create(
            user_id=request.user,
            question_id=question,
            content=data.get('content'),
        )

        return Response(status=status.HTTP_201_CREATED)

class QuestionCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a comment.
    """
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentSerializer

class QuestionResponseList(generics.ListCreateAPIView):
    queryset = QuestionResponse.objects.all().order_by('-timestamp')
    serializer_class = QuestionResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # TODO Move to serializers?    def create(self, validated_data):
        data = request.data

        question = Question.objects.get(id=data.get('question_id'))
        choice = Choice.objects.get(pk=data.get('choice_id'))
        correct = choice.pk == question.answer.pk

        question_response = QuestionResponse.objects.create(
            user_id=request.user,
            correct=correct,
            question_id=question,
            choice_id=choice
        )

        data = {
            'correct': correct,
            **data
        }

        return Response(data, status=status.HTTP_201_CREATED)
