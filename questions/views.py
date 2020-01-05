from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from random import sample
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from questions.models import (
    Question,
    QuestionChoice,
    QuestionResponse,
    QuestionRating,
    QuestionComment,
)
from questions.serializers import (
    QuestionBasicSerializer,
    QuestionDetailSerializer,
    QuestionIdSerializer,
    QuestionResponseCreateSerializer,
    QuestionRatingSerializer,
    QuestionCommentSerializer,
    QuestionResponseListSerializer,
)
from questions.permissions import IsContributorOrReadOnly, IsParentContributorOrReadOnly
from objectives.models import Objective
from utils.utils import paginate


class QuestionListCreate(generics.ListCreateAPIView):
    """ Create a new question.

    # GET

    Returns a paginated list of basic question data.

    ## Query Parameters

    - page (int): Paginated page number
    - objective_id (int): Objective id to filter against

    # POST

    Creates a new question. Creating a new question requires authentication.

    Example body:

        { "objective_id": 3
        , "stem": "string"
        , "choices": 
            [ { "content": "string"
              , "is_correct": true
              , "explanation": "string" }
            , { "content": "string2"
              , "is_correct": false
              , "explanation": "string" } ] }

    ## Responses
    
    ### 201
    The question was successfully created

    """

    # Query from all questions
    queryset = Question.objects.all()

    # Serialize questions using the default question serializer
    # Commented out as this is done manually in the override below.
    # serializer_class = QuestionBasicSerializer

    # Require authentication
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        """ Create a new question from POST request data.

        Overrides the default create method, and bypasses the serializer.
        Might be worth considering whether this could be moved to the
        serializer at some point, but not quite sure how.

        """

        # Get the required information out of the request data
        contributor = request.user
        objective_id = request.data.get("objective_id")
        stem = request.data.get("stem")
        choices = request.data.get("choices")

        # Ensure that each field was present
        if None in [objective_id, stem, choices]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Check whether the objective ID exists
        try:
            objective = Objective.objects.get(id=objective_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Assert that the data is valid
        try:
            # Assert only one correct choice
            correct = [choice for choice in choices if choice["is_correct"]]
            assert len(correct) == 1

            # Assert there is more than one choice
            assert len(choices) > 1

            # Assert that the stem is not blank
            assert stem.strip() != ""

            # Assert that choices are not blank
            choice_blank = [choice.get("content").strip() == "" for choice in choices]
            assert not any(choice_blank)

            # Assert that choices are unique
            choices_content = [choice.get("content").strip() for choice in choices]
            choices_set = set(choices_content)
            assert len(choices_content) == len(choices_set)
        # Return a 400 if any of the tests failed
        except AssertionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create the question
        question = Question.objects.create(
            contributor=contributor, objective=objective, stem=stem
        )

        # Create each question choice for the created question
        for choice in choices:
            QuestionChoice.objects.create(question=question, **choice)

        # Serialize the added question
        serialized = QuestionBasicSerializer(question)

        # Return the serialized question
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """ Return a list of basic question data with filters applied.

        This only retrieves basic information about the question without any of
        its linked information.

        """

        # Get the queryset from the specified parent queryset.
        queryset = super().get_queryset()

        # Get query params, and set to default if not specified
        objective_id = request.GET.get("objective_id")
        page = int(request.GET.get("page") or 0) or 1

        # Filter the queryset
        if objective_id:
            filtered_questions = queryset.filter(
                Q(objective__id=objective_id)
            )
        else:
            filtered_questions = queryset

        data = paginate(page, filtered_questions, QuestionBasicSerializer)

        # Return a HTTP response
        return Response(data, status=status.HTTP_200_OK)



class QuestionIdList(generics.ListAPIView):
    """ Retrieves a list of question IDs.

    This endpoint is public and returns a list of IDs only (not the full
    serialized question). This is intended for generating a list of Question
    IDs for a test.

    # GET
    Retrieve a list of question IDs.

    ## Query Parameters
    
    - quantity (int): The number of question IDs, default 10
    - random (bool: "true" or "false"): Whether to randomly sample from IDs, default false
    - specialty (int): Filtered specialties, default all
    - topic (int): Filtered topics, default all
    - stage (int): Filtered stages, default all

    Example URL: `/questions/?quantity=5&random=true&specialty=1&specialty=2&topic=3

    """

    # Query from all Question objects
    queryset = Question.objects.all()

    # Use the Question Id
    serializer_class = QuestionIdSerializer

    def list(self, request, *args, **kwargs):
        """ Return a list of question IDs to create a question test. 
        """

        # Get the queryset from the specified parent queryset.
        queryset = super().get_queryset()

        # Get query params, and set to default if not specified
        quantity = int(request.GET.get("quantity") or 0) or 10
        random = request.GET.get("random")
        specialties = request.GET.getlist("specialty") or [
            ch[0] for ch in Objective.SPECIALTY_CHOICES
        ]
        topics = request.GET.getlist("topic") or [
            ch[0] for ch in Objective.TOPIC_CHOICES
        ]
        stage = request.GET.getlist("stage") or [
            ch[0] for ch in Objective.STAGE_CHOICES
        ]

        # Filter the queryset by specialty, topic and stage
        filtered_questions = queryset.filter(
            Q(objective__specialty__in=specialties)
            & Q(objective__topic__in=topics)
            & Q(objective__stage__in=stage)
        )

        # Convert the filtered questions to their IDs
        question_ids = list(filtered_questions.values_list("id", flat=True))

        # Guard against if the quantity is greater than the number of ids
        quantity_safe = min(quantity, len(question_ids))

        # Get the quantity of IDs, depending on if random or not
        if random:
            selected_ids = sample(question_ids, quantity_safe)
        else:
            selected_ids = question_ids[:quantity_safe]

        # Return the IDs in a 200 response
        return Response(selected_ids, status=status.HTTP_200_OK)


class QuestionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieves a single detailed question.

    This is the basic endpoint for when a question is encountered during a
    test. It includes all linked information such as choices and comments.

    """

    # Query from all Question objects
    queryset = Question.objects.all()

    # Serialize with the detailed question serializer
    serializer_class = QuestionDetailSerializer


    # Only the contributor can update the question
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsContributorOrReadOnly,
    )

class QuestionRatingCreate(generics.CreateAPIView):
    """ Create a new question rating.

    # POST

    Example Body: 

        { "question": 3
        , "rating": 4 }

    """

    # Use the default question rating serializer
    serializer_class = QuestionRatingSerializer


class QuestionCommentCreate(generics.CreateAPIView):
    """ Create a comment on a question.

    # POST

    Example Body:

        { "question": 3
        , "content": "string" }

    """

    # Use the default question comment serializer
    serializer_class = QuestionCommentSerializer


class QuestionResponseListCreate(generics.ListCreateAPIView):
    """ Create a new question response.

    The only required information is the choice ID. 

    # POST

    Example Body:

        { "choice": 3 }

    # GET


    """

    # Query all question responses
    queryset = QuestionResponse.objects.all()

    def get_serializer_class(self):
        """ Use a different serializer based on request type.
        """
        if self.request.method == "POST":
            serializer_class = QuestionResponseCreateSerializer
        else:  
            serializer_class = QuestionResponseListSerializer
        return serializer_class

    def get_permissions(self):
        """ Use different permissions based on request type.
        """
        if self.request.method == "POST":
            permission_classes = (permissions.AllowAny(),)
        else:
            permission_classes = (permissions.IsAuthenticated(),)
        return permission_classes

    def get_queryset(self):
        # Get the user from the request
        user = self.request.user

        # Filter by the user and order by response submission time
        queryset = self.queryset.filter(user=user).order_by("-created_at")
        return queryset


class QuestionAccuracyRetrieve(generics.RetrieveAPIView):
    """ Returns question accuracy by specialty, topic and stage.


    # GET

    ## Query Parameters
    
    - group (str): one of "specialty", "topic" or "stage"

    Example URL: `/accuracy/?group=specialty
    
    """

    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):

        # Get group from query parameter
        group = self.request.GET.get("group")

        # Match the group against the type of grouping
        if group == "specialty":
            values = Objective.objects.values("specialty")
        elif group == "topic":
            values = Objective.objects.values("topic")
        elif group == "stage":
            values = Objective.objects.values("stage")
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)

        # Get the user from the request
        user = request.user

        # Annotate correct and incorrect values based on the grouping
        accuracy = values.annotate(
            correct=Count(
                "objective_question__question_choice__choice_response",
                filter=Q(
                    objective_question__question_choice__choice_response__user=user
                )
                & Q(
                    objective_question__question_choice__choice_response__choice__is_correct=True
                ),
            ),
            incorrect=Count(
                "objective_question__question_choice__choice_response",
                filter=Q(
                    objective_question__question_choice__choice_response__user=user
                )
                & Q(
                    objective_question__question_choice__choice_response__choice__is_correct=False
                ),
            ),
        )

        return Response(accuracy, status=status.HTTP_200_OK)
