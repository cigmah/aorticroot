from rest_framework import serializers
from questions.models import *
from tags.models import Tag
from choices.models import Choice
from tags.serializers import TagSerializer
from choices.serializers import ChoiceSerializer
from users.serializers import UserSerializer
from django.contrib.auth.models import User


class QuestionCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = QuestionComment
        fields = ('user', 'content', 'timestamp')
        read_only_fields = ('timestamp',)

class QuestionLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id')

    class Meta:
        model = QuestionLike
        fields = ('user',)

class QuestionTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(source='tag_id')

    class Meta:
        model = QuestionTag
        fields = ('tag',)

    def to_representation(self, instance):
        original = super().to_representation(instance)
        return original.pop('tag')

class QuestionDistractorSerializer(serializers.ModelSerializer):
    distractor = ChoiceSerializer(source='choice_id')

    class Meta:
        model = QuestionDistractor
        fields = ('distractor', 'explanation')

    def to_representation(self, instance):
        original = super().to_representation(instance)
        popped = original.pop('distractor')
        popped['explanation'] = original['explanation']
        return popped

class QuestionSerializer(serializers.ModelSerializer):
    tags = QuestionTagSerializer(many=True, read_only=True)
    distractors = QuestionDistractorSerializer(many=True, read_only=True)
    comments = QuestionCommentSerializer(many=True, read_only=True)
    likes = QuestionLikeSerializer(many=True, read_only=True)
    user_id = UserSerializer(read_only=True)
    answer = ChoiceSerializer()

    class Meta:
        model = Question
        fields = '__all__'

class QuestionResponseSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    question_id = QuestionSerializer(read_only=True)
    choice_id = ChoiceSerializer(read_only=True)
    class Meta:
        model = QuestionResponse
        fields = '__all__'
