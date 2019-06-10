from questions.models import *
from questions.serializers import *
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class QuestionList(generics.ListCreateAPIView):
    """
    List all questions, or create a new question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('tags', 'stem', 'answer', 'explanation')
    filter_fields = ('tags', 'user_id', )

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

class QuestionCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates or deletes a comment.
    """
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentSerializer
