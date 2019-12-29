from rest_framework import serializers
from users.serializers import UserSerializer
from objectives.serializers import ObjectiveSerializer
from questions.models import (
    Question,
    QuestionChoice,
    QuestionComment,
    QuestionRating,
    QuestionResponse,
)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """ The default serializer for a question choice.
    """

    # A field for the number of times a choice was chosen.
    num_chosen = serializers.SerializerMethodField()

    class Meta:
        model = QuestionChoice
        fields = (
            "id",
            "question",
            "content",
            "explanation",
            "is_correct",
            "num_chosen",
        )
        read_only_fields = (
            "id",
            "num_chosen",
        )

    def get_num_chosen(self, object):
        """ Get the number of times this choice was chosen.
        """
        return object.choice_response.count()


class QuestionCommentSerializer(serializers.ModelSerializer):
    """ The default serializer for a question comment.
    """

    # Serialize the author using the User serializer
    contributor = UserSerializer(required=False)

    class Meta:
        model = QuestionComment
        fields = (
            "question",
            "contributor",
            "created_at",
            "content",
        )
        read_only_fields = (
            "created_at",
            "contributor",
        )

    def create(self, validated_data):
        """ Get the user from the request on creation.
        """
        contributor = self.context["request"].user

        # Anonymous comments are permitted
        if contributor.is_authenticated:
            question_comment = QuestionComment.objects.create(
                contributor=contributor, **validated_data
            )
        else:
            question_comment = QuestionComment.objects.create(**validated_data)

        return question_comment


class QuestionRatingSerializer(serializers.ModelSerializer):
    """ The default serializer for a question rating.
    """

    # Serialize the user using the User serializer
    user = UserSerializer(required=False)

    class Meta:
        model = QuestionRating
        fields = (
            "user",
            "question",
            "rating",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):

        # Get the user from the request
        user = self.context["request"].user

        # Anonymous users can also submit ratings
        if user.is_authenticated:
            # If authenticated, then only allow one rating (get or create)
            rating, created = QuestionRating.objects.get_or_create(user=user, **validated_data) 
        else:
            rating = QuestionRating.objects.create(**validated_data)

        return rating


class QuestionBasicSerializer(serializers.ModelSerializer):
    """ A basic serializer for a question.

    This includes only the basic information for a question, without any of its linked 
    information such as comments or choices.

    """

    class Meta:
        model = Question
        fields = (
            "id",
            "objective",
            "contributor",
            "created_at",
            "modified_at",
            "stem",
        )


class QuestionDetailSerializer(serializers.ModelSerializer):
    """ A detailed serializer for a question.

    This should be returned for a full question, and includes the linked
    information such as question choices, ratings and comments.

    """

    # The contributor should be serialized with the default User serializer
    contributor = UserSerializer()

    # The choices should be serialized with the default QuestionChoice serializer
    choices = QuestionChoiceSerializer(source="question_choice", many=True)

    # The comments should be serialized with the default QuestionComment serializer
    comments = QuestionCommentSerializer(source="question_comment", many=True)

    # The objective is fully serialized with the question on read
    objective = ObjectiveSerializer(read_only=True)

    # The average rating should be calculated
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "objective",
            "contributor",
            "created_at",
            "modified_at",
            "stem",
            "choices",
            "comments",
            "average_rating",
        )
        read_only_fields = (
            "id",
            "created_at",
            "modified_at",
            "choices",
            "comments",
            "average_rating",
        )

    def get_average_rating(self, object):
        """ Return the average rating for the given question.
        """
        # Count how many ratings are provided
        count = object.question_rating.count()

        # Protect against a divide by zero error
        if count > 0:
            return object.question_rating.sum() / count
        else:
            return 0


class QuestionIdSerializer(serializers.ModelSerializer):
    """ Serialize a question using only the ID.

    This serializer is for returning a list of questions to create a test.
    Each question is then retrieved individually by the client as the test
    progresses.

    """

    class Meta:
        model = Question
        fields = ("id",)


class QuestionResponseCreateSerializer(serializers.ModelSerializer):
    """ The serializer for creating a question response.

    The only field required is the `choice` ID - the user is obtained from
    the context.

    """

    # Serialize the user with the default User serializer
    user = UserSerializer(required=False)

    class Meta:
        model = QuestionResponse
        fields = (
            "user",
            "choice",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):
        """ Get the user from the request.
        """
        user = self.context["request"].user
        # Allow anonymous response
        if user.is_authenticated:
            response = QuestionResponse.objects.create(user=user, **validated_data)
        else:
            response = QuestionResponse.objects.create(**validated_data)
        return response


class QuestionResponseListSerializer(serializers.ModelSerializer):
    """ The serializer for viewing a list of question responses.

    This is inteded as to serialize responses for viewing as a response
    history to questions, so most of the fields are about the question linked
    to the response.

    """

    # Obtain information about the question that was responded to
    question_id = serializers.ReadOnlyField(source="choice.question.id")
    question_stage = serializers.ReadOnlyField(source="choice.question.stage")
    question_topic = serializers.ReadOnlyField(source="question.note.topic")
    question_specialty = serializers.ReadOnlyField(source="question.note.specialty")

    # Obtain whether the choice was correct or not
    was_correct = serializers.ReadOnlyField(source="choice.is_correct")

    class Meta:
        model = QuestionResponse
        fields = (
            "question_id",
            "question_stage",
            "question_topic",
            "question_specialty",
            "was_correct",
            "created_at",
        )
