from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import *
import random
import string


MAX_USERNAME_LENGTH = 150


class UserTest(APITestCase):
    def setUp(self):

        self.url_create = reverse("user_create")
        self.url_authenticate = reverse("user_authenticate")

    def random_string(self, length):

        characters = string.ascii_letters.join(string.digits)

        result = ''.join(random.choice(characters) for i in range(length))

        return result

    # Helper functions for making users

    def make_user_with_email(self, username, email):

        data = {"username": username, "email": email}

        response = self.client.post(self.url_create, data, format="json")

        return response

    def make_user_without_email(self, username):

        data = {"username": username}

        response = self.client.post(self.url_create, data, format="json")

        return response

    # POST user

    def test_post_user(self):

        response = self.make_user_with_email(self.random_string(MAX_USERNAME_LENGTH), self.random_string(MAX_USERNAME_LENGTH) + "@email.com")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("username", response.data)

        self.assertIn("password", response.data)

        self.assertIn("token", response.data)

    def test_post_user_without_email(self):
        response = self.make_user_without_email(self.random_string(MAX_USERNAME_LENGTH))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("username", response.data)

        self.assertIn("password", response.data)

        self.assertIn("token", response.data)

    def test_post_user_with_space_in_username(self):
        random_string = self.random_string(MAX_USERNAME_LENGTH)

        # replace a random character with a space
        username=random_string.replace(random.choice(random_string), " ", 1)

        response = self.make_user_with_email(username, self.random_string(MAX_USERNAME_LENGTH) + "@email.com")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_user_faulty_email(self):
        response = self.make_user_with_email(self.random_string(MAX_USERNAME_LENGTH),
                                             self.random_string(MAX_USERNAME_LENGTH))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_user_existing_username(self):
        username = self.random_string(MAX_USERNAME_LENGTH)

        self.make_user_with_email(username, self.random_string(MAX_USERNAME_LENGTH) + "@email.com")

        response = self.make_user_with_email(username, self.random_string(MAX_USERNAME_LENGTH) + "@email.com")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # POST authenticate

    def test_post_authenticate(self):

        username = self.random_string(MAX_USERNAME_LENGTH)

        created = self.make_user_with_email(username, self.random_string(MAX_USERNAME_LENGTH) + "@email.com")

        data = {"username": username, "password": created.data.get("password")}

        response = self.client.post(self.url_authenticate, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("token", response.data)

        self.assertIn("username", response.data)


    def test_post_authenticate_incorrect_password(self):

        username = self.random_string(MAX_USERNAME_LENGTH)

        self.make_user_with_email(username, self.random_string(MAX_USERNAME_LENGTH) + "@test.com")

        data = {"username": username, "password": self.random_string(MAX_USERNAME_LENGTH)}

        response = self.client.post(self.url_authenticate, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)