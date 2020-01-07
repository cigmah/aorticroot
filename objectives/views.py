from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from utils.utils import paginate
from objectives.serializers import ObjectiveSerializer
from objectives.models import Objective
from objectives.permissions import IsContributorOrReadOnly


class ObjectiveListCreate(generics.ListCreateAPIView):
    """ List objectives or create a new learning objective.

    All objectives are publicly readable. Creating a new objective requires
    authentication.

    # GET
    Returns a list of learning objectives.

    ## Query Parameters

    - specialty (int, multiple)
    - topic (int, multiple)
    - stage (int, multiple)
    - search (string)
    - page (int)

    ## Responses

    ### 200
    Succesful retrieval. 

    Example response:

        { "count": 2
        , "next" : null
        , "previous": null
        , "results": [
            { "id": 1
            , "specialty": 2
            , "topic": 7
            , "stage": 3
            , "title": "string"
            , "notes": "string"
            , "created_at": "2019-12-29T10:04:08Z"
            , "modified_at": "2019-12-29T10:04:08Z"
            , "num_questions": 0
            , "contributor": 
                { "id": 2
                , "username": "string" } } ] }
    
    # POST
    Create a new learning objective.

    Example body:

        { "specialty": 8
        , "topic": 5 
        , "stage": 3
        , "title": "string"
        , "notes": "string" }

    ## Responses

    ### 201
    Successfully created a new learning objective.

    Example response:

        { "id": 1
        , "specialty": 2
        , "topic": 7
        , "stage": 3
        , "title": "string"
        , "notes": "string"
        , "created_at": "2019-12-29T10:04:08Z"
        , "modified_at": "2019-12-29T10:04:08Z"
        , "num_questions": 0
        , "contributor": 
            { "id": 2
            , "username": "string" } } 

    """

    # Query from all objects
    queryset = Objective.objects.all().order_by("id")

    # Serialize using the default objective serializer
    serializer_class = ObjectiveSerializer

    # Require authentication for creation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        """ Return a list of objectives with filters applied.
        """

        # Get the queryset from the specified parent queryset.
        queryset = super().get_queryset()

        # Get query params, and set to default if not specified
        search = request.GET.get("search")
        page = int(request.GET.get("page") or 0) or 1
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
        if search:
            filtered_objectives = queryset.filter(
                Q(specialty__in=specialties)
                & Q(topic__in=topics)
                & Q(stage__in=stage)
                & (Q(title__contains=search) | Q(contributor__username__contains=search))
            )
        else:
            filtered_objectives = queryset.filter(
                Q(specialty__in=specialties)
                & Q(topic__in=topics)
                & Q(stage__in=stage)
            )

        data = paginate(page, filtered_objectives, ObjectiveSerializer)

        # Return a HTTP response
        return Response(data, status=status.HTTP_200_OK)


class ObjectiveRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or destroy an objective at a given ID.

    All objectives are publicly readable. Modification requires
    authentication as the contributor.

    """

    # Query from all objects
    queryset = Objective.objects.all()

    # Serialize using the default objective serializer
    serializer_class = ObjectiveSerializer

    # Require authentication for creation
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsContributorOrReadOnly,
    )

