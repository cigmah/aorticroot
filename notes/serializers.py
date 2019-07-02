from rest_framework import serializers
from users.serializers import UserSerializer
from notes.models import *


class NoteCommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)

    class Meta:

        model = NoteComment

        fields = "__all__"

        read_only = ("created_at",)

    def create(self, validated_data):
        """
        Get the user from the request on creation.
        """

        author = self.context["request"].user

        note_comment = NoteComment.objects.create(
            author=author,
            **validated_data
        )

        return note_comment

class NoteListSerializer(serializers.ModelSerializer):

    num_questions = serializers.SerializerMethodField()

    num_comments = serializers.SerializerMethodField()

    num_due = serializers.IntegerField(
        default=None
    )

    num_known = serializers.IntegerField(
        default=None
    )

    class Meta:

        model = Note

        fields = (
            'id',
            'title',
            'specialty',
            'topic',
            'modified_at',
            'num_questions',
            'num_comments',
            'num_due',
            'num_known',
        )

    def get_num_questions(self, object):
        return object.note_question.count()

    def get_num_comments(self, object):
        return object.note_comment.count()

class NoteSerializer(serializers.ModelSerializer):

    contributor = UserSerializer(required=False)

    comments = NoteCommentSerializer(
        source="note_comment",
        many=True,
    )

    class Meta:

        model = Note

        fields = (
            'id',
            'title',
            'specialty',
            'topic',
            'content',
            'comments',
            'contributor',
            'modified_at',
        )

