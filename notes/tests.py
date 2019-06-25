from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User


class NoteTest(APITestCase):
    def setUp(self):
        self.url_list_create = reverse("note_list_create")
        self.url_comment_create = reverse("notecomment_create")
        self.make_auth_client()

    def make_auth_client(self):

        # Create a user
        self.user_data = {
            "username": "testQuestion",
            "password": "tester"
        }

        self.user = User.objects.create_user(
            username=self.user_data.get("username"),
            password=self.user_data.get("password"),
        )

        # Get a token
        token_response = self.client.post(
            reverse("user_authenticate"),
            self.user_data,
            format="json",
        )

        self.assertIn(
            "token",
            token_response.data
        )

        self.token = token_response.data.get("token")

        # Create an authenticated client
        self.auth_client = APIClient()

        self.auth_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token
        )

    def test_note_create_valid(self, title="test title"):
        """
        A note with valid data should be accepted.
        """

        data = {
            "year_level": 0,
            "specialty": 1,
            "domain": 2,
            "title": title,
            "content": "test content",
        }

        response = self.auth_client.post(
            self.url_list_create,
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        return response

    def test_note_comment_create_valid(self):
        """
        A note comment with valid data should be accepted.
        """

        created_response = self.test_note_create_valid("test comment")

        note_id = created_response.data.get("id")

        data = {
            "note": note_id,
            "content": "test content"
        }

        response = self.auth_client.post(
            self.url_comment_create,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_note_list(self):
        """
        Listing all notes should succeed (with pagination).
        """

        # TODO
        pass

    def test_note_list_filtered(self):
        """
        Listing all notes with a filter should succeed (with pagination).
        """

        # TODO
        pass

    def test_note_retrieve_with_id(self):
        """
        A note retrieved with an ID should be accepted.
        """

        created_response = self.test_note_create_valid("test retrieve id")

        response = self.client.get(
            reverse(
                "note_retrieve_update_destroy",
                kwargs={"pk": created_response.data["id"]},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
