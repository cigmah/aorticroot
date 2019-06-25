import json
from rest_framework import serializers
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from questions.models import *
from notes.serializers import NoteSerializer
from notes.models import Note


class QuestionChoiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = QuestionChoice

        fields = "__all__"


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

    note = NoteSerializer()

    contributor = UserSerializer()

    choices = QuestionChoiceSerializer(
        source="question_choice",
        many=True
    )

    class Meta:

        model = Question

        fields = "__all__"

        read_only = (
            "created_at",
            "modified_at"
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

        fields = "__all__"

    def create(self, validated_data):
        """
        Get the user from the request.
        """

        user = self.context["request"].user

        response = QuestionResponse.objects.create(
            user=user,
            **validated_data
        )

        return response
