""" Serializers for the Objective models.
"""

from rest_framework import serializers
from users.serializers import UserSerializer
from objectives.models import Objective


class ObjectiveSerializer(serializers.ModelSerializer):
    """ The default serializer for a learning Objective.
    """

    contributor = UserSerializer(required=False)
    num_questions = serializers.SerializerMethodField()

    class Meta:
        model = Objective
        fields = (
            "id",
            "title",
            "specialty",
            "topic",
            "stage",
            "notes",
            "contributor",
            "created_at",
            "modified_at",
            "num_questions",
        )
        read_only_fields = (
            "id",
            "contributor",
            "created_at",
            "modified_at",
            "num_questions",
        )

    def create(self, validated_data):
        """ Create a new objective, retrieving the user from the request.
        """
        contributor = self.context["request"].user
        objective = Objective.objects.create(contributor=contributor, **validated_data)
        return objective

    def get_num_questions(self, object):
        """ Get the number of questions allocated under this objective.
        """
        return object.objective_question.count()
