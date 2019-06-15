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
        read_only_fields = ('timestamp',)

    def create(self, validated_data):
        user = self.context['request'].user

        question_comment = QuestionComment.objects.create(
            user=user,
            **validated_data
        )

        return question_comment

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

class QuestionResponseSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()

    class Meta:
        model = QuestionResponse
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        
        correct_answer = Question.objects.get(id=validated_data.get('question_id'))
        correct = validated_data.get('choice_id') == correct_answer.id

        question_response = QuestionResponse.objects.create(
            user_id=user,
            correct=correct,
            **validated_data
        )

        return question_response
