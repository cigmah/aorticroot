import random
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.tests import UserTest
from objectives.models import Objective


class ObjectiveTest(UserTest):
    """ The base objective test class with helpers.

    This inherits from UserTest which provides helpers to create a user. 
    """

    def setUp(self):
        super().setUp()
        # Store the necessary urls into easily accessible variables
        self.url_objective_list = reverse("objective_list_create")
        self.url_objective_create = reverse("objective_list_create")

        # Create a user for use with objective tests
        self.username = "objective_test"
        response = self.create_user_without_email(self.username)

        # Create an authenticated client
        self.auth_client = APIClient()
        self.auth_client.credentials(
            HTTP_AUTHORIZATION="Token " + response.data.get("token")
        )

        # Create another authenticated client, "other"
        self.other_username = "objective_test_other"
        other_response = self.create_user_without_email(self.other_username)
        self.auth_client_other = APIClient()
        self.auth_client_other.credentials(
            HTTP_AUTHORIZATION="Token " + other_response.data.get("token")
        )

        # Create a default objective
        data = self.create_random_objective_data()
        response = self.create_objective(data)
        self.default_objective = response.data

    def url_objective_retrieve(self, pk: int):
        return reverse("objective_retrieve_update_destroy", kwargs={"pk": pk})

    def url_objective_update(self, pk: int):
        return reverse("objective_retrieve_update_destroy", kwargs={"pk": pk})

    def url_objective_destroy(self, pk: int):
        return reverse("objective_retrieve_update_destroy", kwargs={"pk": pk})

    def create_objective(self, data):
        """ Create an objective from given data.
        """
        response = self.auth_client.post(self.url_objective_create, data, format="json")
        return response

    def create_random_objective_data(self):
        """ Create random objective data
        """
        data = {
            "specialty": random.choice(Objective.SPECIALTY_CHOICES)[0],
            "topic": random.choice(Objective.TOPIC_CHOICES)[0],
            "stage": random.choice(Objective.STAGE_CHOICES)[0],
            "title": get_random_string(),
            "notes": get_random_string(),
        }
        return data


class ObjectiveCreateTest(ObjectiveTest):
    """ Test creating objectives.
    """

    def test_post_objective_valid(self):
        """ POST to create a new objective should return 201 if the required information is present.
        """
        data = self.create_random_objective_data()
        response = self.create_objective(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("specialty", response.data)
        self.assertIn("topic", response.data)
        self.assertIn("stage", response.data)
        self.assertIn("title", response.data)
        self.assertIn("notes", response.data)

    def test_post_objective_invalid(self):
        """ POST to create a new objective should return 400 if incomplete data is provided.
        """
        data = self.create_random_objective_data()

        # Delete the specialty key from the data
        data.pop("specialty")

        response = self.create_objective(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_objective_unauthenticated(self):
        """ POST to create a new objective should return 401 if the user is not authenticated.
        """
        data = self.create_random_objective_data()
        response = self.client.post(self.url_objective_create, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_objective_title_not_unique(self):
        """ POST to create a new objective should return a 400 if the title conflicts with another objective.
        """
        data = self.create_random_objective_data()
        
        # Create the objective
        self.create_objective(data)

        # Create the same objective
        response = self.create_objective(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ObjectiveListTest(ObjectiveTest):
    """ Test listing objectives.
    """

    def test_get_objective_list(self):
        """ GET to list all objectives should return 200.
        """

        data_1 = self.create_random_objective_data()
        data_2 = self.create_random_objective_data()
        self.create_objective(data_1)
        self.create_objective(data_2)

        # Authentication is not required, so use the default client
        response = self.client.get(self.url_objective_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert there is more than one objective listed
        results = response.data.get("results")
        self.assertGreater(len(results), 1)


class ObjectiveRetrieveTest(ObjectiveTest):
    """ Test retrieving an objective.
    """

    def test_get_objective_by_id(self):
        """ GET to retrieve a single objective should return 200.
        """

        data = self.create_random_objective_data()
        create_response = self.create_objective(data)
        objective_id = create_response.data.get("id")

        response = self.client.get(self.url_objective_retrieve(objective_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ObjectiveUpdateTest(ObjectiveTest):
    """ Test updating an objective.
    """
    def test_update_objective_by_contributor(self):
        """ The contributor should be able to update an objective, returning 200.
        """
        objective_id = self.default_objective.get("id")
        new_notes = get_random_string()
        data = { "notes": new_notes }
        response = self.auth_client.patch(self.url_objective_update(objective_id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("notes"), new_notes)

    def test_update_objective_by_other(self):
        """ A different user should not be able to update an objective, returning 403.
        """
        objective_id = self.default_objective.get("id")
        new_notes = get_random_string()
        data = { "notes": new_notes }
        response = self.auth_client_other.patch(self.url_objective_update(objective_id), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ObjectiveDestroyTest(ObjectiveTest):
    """ Test destroying an objective.
    """

    def test_destroy_objective_by_contributor(self):
        """ The contributor should be able to destroy an objective, returning 204.
        """
        objective_id = self.default_objective.get("id")
        response = self.auth_client.delete(self.url_objective_destroy(objective_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_objective_by_other(self):
        """ A different user should not be able to destroy an objective, returning 403.
        """
        objective_id = self.default_objective.get("id")
        response = self.auth_client_other.delete(self.url_objective_destroy(objective_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
