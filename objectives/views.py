from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from objectives.serializers import ObjectiveSerializer
from objectives.models import Objective
from objectives.permissions import IsContributorOrReadOnly

class ObjectiveListCreate(generics.ListCreateAPIView):
    """ List objectives or create a new learning objective.

    All objectives are publicly readable. Creating a new objective requires
    authentication.

    # GET
    Returns a list of learning objectives. 

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

