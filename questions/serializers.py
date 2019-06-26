import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from questions.models import *
from notes.serializers import NoteSerializer
from notes.models import Note


class QuestionChoiceSerializer(serializers.ModelSerializer):

    num_chosen = serializers.SerializerMethodField()

    class Meta:

        model = QuestionChoice

        fields = "__all__"

    def get_num_chosen(self, object):
        return object.choice_response.count()

class QuestionCommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)

    class Meta:

        model = QuestionComment

        fields = "__all__"

        read_only = ("created_at",)

    def create(self, validated_data):
        """
        Get the user from the request on creation.
        """

        author = self.context["request"].user

        question_comment = QuestionComment.objects.create(
            author=author,
            **validated_data
        )

        return question_comment

class QuestionLikeSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        required=False,
        read_only=True
    )

    class Meta:

        model = QuestionLike

        fields = "__all__"

    def create(self, validated_data):

        user = self.context["request"].user

        like = QuestionLike.objects.create(
            user=user,
            **validated_data
        )

        return like


class QuestionFlagSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        required=False,
        read_only=True
    )

    class Meta:
        model = QuestionFlag
        fields = "__all__"

    def create(self, validated_data):

        user = self.context["request"].user

        flag = QuestionFlag.objects.create(
            user=user,
            **validated_data
        )

        return flag


class QuestionSerializer(serializers.ModelSerializer):

    contributor = UserSerializer()

    choices = QuestionChoiceSerializer(
        source="question_choice",
        many=True
    )

    comments=QuestionCommentSerializer(
        source='question_comment',
        many=True,
    )

    num_likes = serializers.IntegerField(
        default=None
    )

    liked = serializers.BooleanField(
        default=None
    )

    num_seen = serializers.IntegerField(
        default=None
    )

    class Meta:

        model = Question

        fields = (
            'note',
            'contributor',
            'id',
            'stem',
            'choices',
            'comments',
            'num_likes',
            'liked',
            'num_seen',
            'modified_at'
        )

class QuestionIdSerializer(serializers.ModelSerializer):

    class Meta:

        model = Question

        fields = (
            'id',
        )

class QuestionResponseSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True
    )

    class Meta:

        model = QuestionResponse

        fields = (
            'question',
            'user',
            'choice',
            'ease',
            'interval_days',
            'next_due_datetime'
        )

        read_only = (
            'ease',
            'interval_days',
            'next_due_datetime',
        )

    def calculate_new_ease(self, old_ease, q):
        return old_ease - 0.8 + (0.28 * q - 0.02 * q * q)

    def create(self, validated_data):
        """
        Get the user from the request.
        """

        user = self.context["request"].user

        try:
            correct_choice = QuestionChoice.objects.filter(
                question__id=validated_data.get("question").id,
                is_correct=True,
            ).get()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        correct = validated_data.get("choice") ==  correct_choice.id

        try:
            last = QuestionResponse.objects.filter(
                question__id=validated_data.get("question").id,
                user=user
            ).order_by('-next_due_datetime')[0]

            new_interval = last.interval_days * last.ease

            if correct:
                new_ease = self.calculate_new_ease(last.ease, 3)
            else:
                new_ease = self.calculate_new_ease(last.ease, 0)

        except IndexError:
            new_interval = 1
            new_ease = 2.5

        next_due_datetime = timezone.now() + timedelta(days=new_interval)

        response = QuestionResponse.objects.create(
            user=user,
            interval_days=new_interval,
            next_due_datetime=next_due_datetime,
            **validated_data
        )

        return response
