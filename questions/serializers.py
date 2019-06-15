from rest_framework import serializers
from questions.models import *
from tags.models import Tag
from choices.models import Choice
from tags.serializers import TagSerializer
from choices.serializers import ChoiceSerializer
from users.serializers import UserSerializer
from django.contrib.auth.models import User


class QuestionCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id')

    class Meta:
        model = QuestionComment
        fields = ('user', 'content', 'timestamp')

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
        fields = ('distractor',)

    def to_representation(self, instance):
        original = super().to_representation(instance)
        return original.pop('distractor')

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
