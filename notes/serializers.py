from rest_framework import serializers
from users.serializers import UserSerializer
from notes.models import *

class NoteCommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(
        required=False
    )

    class Meta:
        model = NoteComment
        fields = '__all__'
        read_only = ('created_at',)

    def create(self, validated_data):
        """
        Get the user from the request on creation.
        """

        author = self.context['request'].user

        note_comment = NoteComment.objects.create(
            author=author,
            **validated_data
        )

        return note_comment

class NoteSerializer(serializers.ModelSerializer):

    contributor = UserSerializer(
        required=False
    )

    comments = NoteCommentSerializer(
        source='notecomment_set',
        many=True,
        required=False
    )

    class Meta:
        model = Note
        fields = '__all__'
        read_only = ('created_at', 'modified_at', 'comments', 'contributor')

    def create(self, validated_data):
        """
        Automatically get the user from the request on creation.
        """

        contributor = self.context['request'].user

        note = Note.objects.create(
            contributor=contributor,
            **validated_data
        )

        return note
