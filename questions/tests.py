from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from questions.models import *
from notes.models import Note


class QuestionTest(APITestCase):
    def setUp(self):

        self.url_list_create = reverse("question_list_create")
        self.url_random_list = reverse("question_random_list")
        self.url_response_create = reverse("question_response_create")
        self.url_like_create = reverse("question_like_create")
        self.url_flag_create = reverse("question_flag_create")

        self.make_auth_client()

        self.note = Note.objects.create(
            contributor=self.user,
            year_level=0,
            specialty=1,
            domain=2,
            title="test note",
            content="test content",
        )

    def make_auth_client(self):

        # Create a user
        self.user_data = {"username": "testQuestion", "password": "tester"}

        self.user = User.objects.create_user(
            username=self.user_data.get("username"),
            password=self.user_data.get("password"),
        )

        # Get a token
        token_response = self.client.post(
            reverse("user_authenticate"), self.user_data, format="json"
        )

        self.assertIn("token", token_response.data)

        self.token = token_response.data.get("token")

        # Create an authenticated client
        self.auth_client = APIClient()

        self.auth_client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_question_valid(self):
        """
        Creating a valid question should pass.
        """

        data = {
            "note_id": self.note.id,
            "stem": "test stem",
            "choices": [
                {
                    "content": "test choice",
                    "explanation": "test explanation",
                    "is_correct": True,
                },
                {
                    "content": "test choice 2",
                    "explanation": "test explanation",
                    "is_correct": False,
                },
                {
                    "content": "test choice 3",
                    "explanation": "test explanation",
                    "is_correct": False,
                },
            ],
        }

        response = self.auth_client.post(self.url_list_create, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response

    def test_get_question(self):
        """
        Getting a question by ID should pass.
        """

        created_response = self.test_create_question_valid()

        response = self.client.get(
            reverse(
                "question_retrieve_update_destroy",
                kwargs={"pk": created_response.data["id"]},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response

    def test_post_question_response(self):
        """
        Posting a response to a question should pass.
        """

        got_question_response = self.test_get_question()

        data = {
            "question": got_question_response.data["id"],
            "choice": got_question_response.data["choices"][0]["id"],
        }

        response = self.auth_client.post(self.url_response_create, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_question_like(self):
        """
        Posting a like to a question should pass.
        """

        created_response = self.test_create_question_valid()

        data = {"question": created_response.data["id"]}

        response = self.auth_client.post(self.url_like_create, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_question_flag(self):
        """
        Posting a flag to a question should pass.
        """

        created_response = self.test_create_question_valid()

        data = {"question": created_response.data["id"]}

        response = self.auth_client.post(self.url_flag_create, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_random_list(self):
        """
        Getting a random list of IDs should pass.
        """

        created_response = self.test_create_question_valid()

        data = {"quantity": 5}

        response = self.auth_client.get(self.url_random_list, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
