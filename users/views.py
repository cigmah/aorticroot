""" Handles operations relating to user management.
"""

from django.contrib.auth.models import User
from django.core.validators import validate_email, validate_slug
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    """ Creates a new user.

    This view requires only a username from the request object and can take
    an optional email. The username and email are both validated, a random
    password is generated, the user object is created in the database, an
    initial token is generated, and the username, token and password are
    returned from the response.

    # POST
    Submit new user details to create a new user.

    Example Body:

        { "username": "string"
        , "email": "string" }

    ## Responses

    ### 400
    Invalid username or email.

    ### 409
    Username or email already taken.

    ### 201
    Successfully created.

    Example Response:

        { "username": "string" 
        , "password": "string"
        , "token": "string" }
   
    """

    # Query from all Users
    queryset = User.objects.all()

    # Use the User serializer
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        # Retrieve request parameters
        username = request.data.get("username")
        email = request.data.get("email")

        # Validate the username
        try:
            validate_slug(username)
        except ValidationError:
            return Response({"invalid": "username"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the email, if an email is provided
        if email is not None and email != "":
            try:
                validate_email(email)
            except ValidationError:
                return Response(
                    {"invalid": "email"}, status=status.HTTP_400_BAD_REQUEST
                )

        # Generate a random password
        password = User.objects.make_random_password()

        # Create a new user
        try:
            user = User.objects.create_user(username, email, password=password)
        except IntegrityError:
            return Response(
                {"invalid": "username or email"}, status=status.HTTP_409_CONFLICT
            )

        # Generate a new token
        token = Token.objects.create(user=user)

        # Return 201 response
        data = {"username": user.username, "token": token.key, "password": password}
        return Response(data, status=status.HTTP_201_CREATED)


class Authenticate(ObtainAuthToken):
    """ Authenticates a user.

    This view allows a user to retrieve a new token by providing their
    username and password.

    # POST
    Submit credentials to obtain a new authentication token.

    Example Body:

        { "username": "string" 
        , "password": "string" }

    ## Responses

    ### 400
    Invalid request data.

    ### 200
    Successfully authenticated.

    Example Response:

        { "username": "string"
        , "token": "string" }

    """

    def post(self, request, *args, **kwargs):

        # Attempt to serialize the received data
        serialized = self.serializer_class(
            data=request.data, context={"request": request}
        )

        # Raise an exception (automatically 400) if invalid data
        serialized.is_valid(raise_exception=True)

        # Get or create a new token
        user = serialized.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        # Return a 200 response
        return Response(
            {"token": token.key, "username": user.username,}, status=status.HTTP_200_OK
        )


class UserStatistic(generics.RetrieveAPIView):
    """ Gets user statistics.
    """

    pass
