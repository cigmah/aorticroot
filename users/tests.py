""" Tests for the User endpoints.
"""

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase
from rest_framework import status
import random


MAX_USERNAME_LENGTH = 150


class UserTest(APITestCase):
    """ The base user test class with helpers.
    """
    def setUp(self):
        self.url_user_create = reverse("user_create")
        self.url_user_authenticate = reverse("user_authenticate")

    def create_user_with_email(self, username, email):
        """ Create a user with a username and email via a POST request.
        """
        data = {"username": username, "email": email}
        response = self.client.post(self.url_user_create, data, format="json")
        return response

    def create_user_without_email(self, username):
        """ Create a user with only a username via a POST request.
        """
        data = {"username": username}
        response = self.client.post(self.url_user_create, data, format="json")
        return response


class UserCreateTest(UserTest):
    """ Tests related to user creation under the UserCreate view.
    """
    def test_post_user(self):
        """ Creating a user with a username and email should return 201.
        """
        response = self.create_user_with_email(
            get_random_string(length=MAX_USERNAME_LENGTH),
            get_random_string(length=MAX_USERNAME_LENGTH) + "@email.com",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertIn("token", response.data)

    def test_post_user_without_email(self):
        """ Creating a user with a username only should return 201.
        """
        response = self.create_user_without_email(get_random_string(length=MAX_USERNAME_LENGTH))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertIn("token", response.data)

    def test_post_user_with_space_in_username(self):
        """ Creating a user with a space in the username should return 400.
        """
        random_string = get_random_string(length=MAX_USERNAME_LENGTH)

        # replace a random character with a space
        username = random_string.replace(random.choice(random_string), " ", 1)

        response = self.create_user_with_email(
            username, get_random_string(length=MAX_USERNAME_LENGTH) + "@email.com"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_user_faulty_email(self):
        """ Creating a user with an invalid email should return 400 (no @ symbol).
        """
        response = self.create_user_with_email(
            get_random_string(length=MAX_USERNAME_LENGTH),
            get_random_string(length=MAX_USERNAME_LENGTH),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_user_existing_username(self):
        """ Creating a user with a taken username should return 409.
        """
        username = get_random_string(length=MAX_USERNAME_LENGTH)
        self.create_user_with_email(
            username, get_random_string(length=MAX_USERNAME_LENGTH) + "@email.com"
        )
        response = self.create_user_with_email(
            username, get_random_string(length=MAX_USERNAME_LENGTH) + "@email.com"
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

class UserAuthenticateTest(UserTest):
    """ Tests for user authentication through the Authenticate view.
    """
    def test_post_authenticate(self):
        """ Authenticating with a correct username and password should return 200.
        """
        # Create a new user
        username = get_random_string(length=MAX_USERNAME_LENGTH)
        created = self.create_user_with_email(
            username, get_random_string(length=MAX_USERNAME_LENGTH) + "@email.com"
        )

        # Attempt to re-authenticated
        data = {"username": username, "password": created.data.get("password")}
        response = self.client.post(self.url_user_authenticate, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)

    def test_post_authenticate_incorrect_password(self):
        """ Authenticating with an incorrect password should return 400.
        """
        username = get_random_string(length=MAX_USERNAME_LENGTH)
        self.create_user_with_email(
            username, get_random_string(length=MAX_USERNAME_LENGTH) + "@test.com"
        )
        data = {
            "username": username,
            "password": get_random_string(length=MAX_USERNAME_LENGTH),
        }
        response = self.client.post(self.url_user_authenticate, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)