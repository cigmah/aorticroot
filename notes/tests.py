from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from notes.models import *
from questions.models import *
from datetime import timedelta
import random

MIN_YEAR_LEVEL = 0
MAX_YEAR_LEVEL = 5
MIN_SPECIALTY = 0
MAX_SPECIALTY = 28

class NoteTest(APITestCase):
    def setUp(self):
        self.url_list = reverse("note_list")
        self.url_comment_create = reverse("notecomment_create")
        self.make_auth_client()

        # Create a default note
        self.default_note = Note.objects.create(
            contributor=None,
            year_level=Note.GENERAL_YEAR_LEVEL,
            specialty=Note.GENERAL_SPECIALTY,
            title="Test title",
            content="Test content",
        )


        # Create a default comment
        self.default_comment = NoteComment.objects.create(
            note=self.default_note,
            author=None,
            content="Test comment",
        )

        # Create a question
        self.default_question = Question.objects.create(
            note=self.default_note,
            contributor=None,
            domain=Question.GENERAL_DOMAIN,
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

        # Create a second question
        self.alternative_question = Question.objects.create(
            note=self.default_note,
            contributor=None,
            domain=Question.GENERAL_DOMAIN,
            stem="Test stem 2",
        )

        # Create a second question choice
        self.alternative_choice = QuestionChoice.objects.create(
            question=self.alternative_question,
            content="Test choice",
            explanation=None,
            is_correct=True,
        )

        # Create another response, in the past.
        self.alternative_response = QuestionResponse.objects.create(
            user=self.user,
            question=self.alternative_question,
            choice=self.alternative_choice,
            next_due_datetime=timezone.now() - timedelta(days=2)
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

    def test_note_comment_create_valid(self):
        """
        A note comment with valid data should be accepted.
        """

        note_id = self.default_note.id

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

    def test_note_list_without_authentication(self):
        """
        Listing all notes should succeed.
        """

        response = self.client.get(self.url_list)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


    def test_note_list_with_authentication(self):
        """
        Getting a list of notes with authentication should return
        extra data relating to number of questions known and due.
        """

        response = self.auth_client.get(self.url_list)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0].get('num_due'),
            1,
        )

        self.assertEqual(
            response.data[0].get('num_known'),
            1,
        )


    def test_note_list_filtered(self):
        """
        Listing all notes with a filter should succeed (with pagination).
        """

        # Create 60 notes
        for i in range((MAX_YEAR_LEVEL-MIN_YEAR_LEVEL+1)*10):
            Note.objects.create(
                contributor=None,
                year_level=random.randint(MIN_YEAR_LEVEL, MAX_YEAR_LEVEL),
                specialty=random.randint(MIN_SPECIALTY, MAX_SPECIALTY),
                title=i,
                content="",
            )

        # TODO
        for i in range(MIN_SPECIALTY, MAX_YEAR_LEVEL+1):
            response = self.client.get(
                reverse("note_list"),{"year_level":i}
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

            for note in response.data:
                self.assertEqual(note["year_level"], i)

    # test out year level outside of defined levels
    def test_note_list_filtered_invalid_year_level(self):
        response_one_less = self.client.get(
            reverse("note_list"), {"year_level": MIN_YEAR_LEVEL-1}
        )

        self.assertEqual(
            response_one_less.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response_one_less.data),
            0
        )

        response_one_more = self.client.get(
            reverse("note_list"), {"year_level": MAX_YEAR_LEVEL+1}
        )

        self.assertEqual(
            response_one_more.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response_one_more.data),
            0
        )



    def test_note_retrieve_with_id_without_auth(self):
        """
        A note retrieved with an ID should be accepted.
        """

        note_id = self.default_note.id

        response = self.client.get(
            reverse(
                "note_retrieve_update_destroy",
                kwargs={"pk": note_id},
            ),
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_note_retrieve_with_id_with_auth(self):

        note_id = self.default_note.id

        response = self.auth_client.get(
            reverse(
                "note_retrieve_update_destroy",
                kwargs={"pk": note_id},
            ),
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data.get('all_ids')),
            2,
        )

        self.assertEqual(
            len(response.data.get('due_ids')),
            1,
        )

        self.assertEqual(
            len(response.data.get('known_ids')),
            1,
        )
