""" Tests for the Question endpoints.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from questions.models import *
from objectives.tests import ObjectiveTest


class QuestionTest(ObjectiveTest):
    """ Base test for questions. 

    Inherits from ObjectiveTest to provide useful methods for creating
    objectives and a default auth_client.

    """

    def setUp(self):
        super().setUp()
        self.url_question_create = reverse("question_list_create")
        self.url_question_list = reverse("question_list_create")
        self.url_question_test = reverse("question_test")
        self.url_question_rating_create = reverse("question_rating_create")
        self.url_question_comment_create = reverse("question_comment_create")
        self.url_question_response_create = reverse("question_response_list_create")
        self.url_question_response_list = reverse("question_response_list_create")
        self.url_question_accuracy_retrieve = reverse("question_accuracy_retrieve")

        # Create two initial objectives
        self.objective_1, self.objective_2 = self.create_initial_objectives()

        # Create a default question
        created = self.create_default_question()
        create_id = created.get("id")
        read_question = self.client.get(
            self.url_question_retrieve(create_id), format="json"
        )
        self.default_question = read_question.data

    def url_question_retrieve(self, pk):
        return reverse("question_retrieve_update_destroy", kwargs={"pk": pk})

    def url_question_update(self, pk):
        return reverse("question_retrieve_update_destroy", kwargs={"pk": pk})

    def url_question_destroy(self, pk):
        return reverse("question_retrieve_update_destroy", kwargs={"pk": pk})

    def create_initial_objectives(self):
        """ Create an initial set of objectives.
        """

        data_1 = self.create_random_objective_data()
        data_2 = self.create_random_objective_data()
        objective_1 = self.create_objective(data_1)
        objective_2 = self.create_objective(data_2)

        return (objective_1.data, objective_2.data)

    def create_question(self, data):
        """ Create a question from given data.
        """
        response = self.auth_client.post(self.url_question_create, data, format="json")
        return response

    def create_default_question(self):
        """ Create a single default question for testing.
        """
        create_data = self.create_random_question_data(self.objective_1.get("id"))
        create_response = self.create_question(create_data)
        return create_response.data

    def create_random_choice_data(self, is_correct=False):
        """ Create a choice with random content and explanation.
        """
        choice = {
            "content": get_random_string(),
            "explanation": get_random_string(),
            "is_correct": is_correct,
        }
        return choice

    def create_random_question_data(self, objective_id: int, num_choices=3):
        """ Create a question with random stem.
        """

        # Create random choices
        choices = [
            self.create_random_choice_data(is_correct=False)
            for _ in range(num_choices - 1)
        ]
        choices.append(self.create_random_choice_data(is_correct=True))

        question = {
            "objective_id": objective_id,
            "stem": get_random_string(),
            "choices": choices,
        }
        return question


class QuestionCreateTest(QuestionTest):
    """ Tests of question creation.
    """

    def test_create_question_valid(self):
        """ Creating a valid question should return 201.
        """
        # Create question
        data = self.create_random_question_data(self.objective_1.get("id"))

        # Send the request
        response = self.create_question(data)

        # Test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionRetrieveUpdateDestroyTest(QuestionTest):
    """ Test of question retrieval, update and destroy.
    """

    def test_get_question(self):
        """ Getting a question by ID should return 200.
        """

        created = self.create_default_question()
        create_id = created.get("id")

        response = self.client.get(self.url_question_retrieve(create_id), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionIdListTest(QuestionTest):
    """ Test of retrieving question ID lists, i.e. a question test.
    """

    def test_get_question_id_list(self):
        """ Getting a random list of IDs should return 200.
        """
        response = self.client.get(
            self.url_question_test, {"random": "true"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionResponseTest(QuestionTest):
    """ Tests of question responses.
    """

    def test_post_question_response_authenticated(self):
        """ Posting a response to a question should return 201, when authenticated.
        """

        # Retrieve a single choice ID
        read_choices = self.default_question.get("choices")
        choice_id = read_choices[0].get("id")

        # Create a request object
        data = {"choice": choice_id}

        # Send the request
        response = self.auth_client.post(
            self.url_question_response_create, data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_question_response_not_authenticated(self):
        """ Posting a response to a question should also return 201, when not authenticated.
        """

        # Retrieve a single choice ID
        read_choices = self.default_question.get("choices")
        choice_id = read_choices[0].get("id")

        # Create a request object
        data = {"choice": choice_id}

        # Send the request to the anonymous client
        response = self.client.post(
            self.url_question_response_create, data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_response_list(self):
        """ The list of question responses for an authenticated user should return 200.
        """
        response = self.auth_client.get(self.url_question_response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionRatingTest(QuestionTest):
    """ Tests of question ratings.
    """

    def test_post_question_rating_authenticated(self):
        """ Rating a question should return 201, when authenticated.
        """

        # Create a request object
        data = {"question": self.default_question.get("id"), "rating": 3}

        # Send the request
        response = self.auth_client.post(
            self.url_question_rating_create, data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_question_rating_not_authenticated(self):
        """ Rating a question should also return 201, when not authenticated.
        """

        # Create a request object
        data = {"question": self.default_question.get("id"), "rating": 3}

        # Send the request, to the anonymous client
        response = self.client.post(
            self.url_question_rating_create, data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionCommentTest(QuestionTest):
    """ Tests of question comments.
    """

    def test_create_question_comment_authenticated(self):
        """ A question comment with valid data should return 201.
        """

        question_id = self.default_question.get("id")
        data = {"question": question_id, "content": get_random_string()}
        response = self.auth_client.post(
            self.url_question_comment_create, data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_question_comment_not_authenticated(self):
        """ A question comment with valid data should return 201, when not authenticated.
        """
        question_id = self.default_question.get("id")
        data = {"question": question_id, "content": get_random_string()}
        response = self.client.post(
            self.url_question_comment_create, data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionAccuracyTest(QuestionTest):
    """ Tests of question accuracy.
    """

    def test_get_accuracy_specialty(self):
        """ Accuracy by specialty should return 200.
        """

        response = self.auth_client.get(
            self.url_question_accuracy_retrieve, {"group": "specialty"}, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

    def test_get_accuracy_topic(self):
        """ Accuracy by topic should return 200.
        """

        response = self.auth_client.get(
            self.url_question_accuracy_retrieve, {"group": "topic"}, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

    def test_get_accuracy_stage(self):
        """ Accuracy by stage should return 200.
        """

        response = self.auth_client.get(
            self.url_question_accuracy_retrieve, {"group": "stage"}, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

