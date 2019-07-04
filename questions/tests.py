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
        self.url_random = reverse("question_random")
        self.url_response_create = reverse("question_response_create")
        self.url_like_create = reverse("question_like_create")
        self.url_flag_create = reverse("question_flag_create")
        self.url_comment_create = reverse("question_comment_create")

        self.make_auth_client()

        # Initialise notes
        for specialty in Note.SPECIALTY_CHOICES:
            for topic in Note.TOPIC_CHOICES:

                title = (
                    specialty[1].lower().replace("_"," ").title() +
                    " - " +
                    topic[1].lower().replace("_", " ").title()
                )

                Note.objects.get_or_create(
                    specialty=specialty[0],
                    topic=topic[0],
                    title=title,
                    content="",
                )


        self.default_note = Note.objects.filter(id=1).get()

        # Create a question
        self.default_question = Question.objects.create(
            note=self.default_note,
            contributor=None,
            domain=Question.GENERAL_DOMAIN,
            year_level=Question.GENERAL_YEAR_LEVEL,
            stem="Test stem",
        )

        # Create a question choice
        self.default_choice = QuestionChoice.objects.create(
            question=self.default_question,
            content="Test choice",
            explanation=None,
            is_correct=True,
        )

        # Create a default response,
        self.default_response = QuestionResponse.objects.create(
            user=self.user,
            question=self.default_question,
            choice=self.default_choice,
        )

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
            self.user_data, format="json"
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

    def test_create_question_valid(self):
        """
        Creating a valid question should pass.
        """

        data = {
            "note_id": self.default_note.id,
            "stem": "test stem",
            "domain": Question.GENERAL_DOMAIN,
            "year_level": Question.GENERAL_YEAR_LEVEL,
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

        response = self.auth_client.post(
            self.url_list_create,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        return response

    def test_get_question(self):
        """
        Getting a question by ID should pass.
        """

        response = self.client.get(
            reverse(
                "question_retrieve_update_destroy",
                kwargs={"pk": self.default_question.id},
            ),
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            'num_chosen',
            response.data.get("choices")[0],
        )

        return response

    def test_get_question_with_auth(self):
        """
        Getting a question while authenticated should pass.
        """

        response = self.auth_client.get(
            reverse(
                "question_retrieve_update_destroy",
                kwargs={"pk": self.default_question.id},
            ),
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_post_question_response(self):
        """
        Posting a response to a question should pass.
        """

        got_question_response = self.test_get_question()

        data = {
            "question": got_question_response.data["id"],
            "choice": got_question_response.data["choices"][0]["id"],
        }

        response = self.auth_client.post(
            self.url_response_create,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_post_question_like(self):
        """
        Posting a like to a question should pass.
        """

        created_response = self.test_create_question_valid()

        data = {
            "question": created_response.data["id"]
        }

        response = self.auth_client.post(
            self.url_like_create,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_post_question_flag(self):
        """
        Posting a flag to a question should pass.
        """

        created_response = self.test_create_question_valid()

        data = {
            "question": created_response.data["id"]
        }

        response = self.auth_client.post(
            self.url_flag_create,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_question_random(self):
        """
        Getting a random question should pass.
        """

        created_response = self.test_create_question_valid()

        response = self.auth_client.get(
            self.url_random,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_comment_create_valid(self):
        """
        A question comment with valid data should be accepted.
        """

        question_id = self.default_question.id

        data = {
            "question": question_id,
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
