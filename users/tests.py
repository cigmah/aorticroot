from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import *


class UserTest(APITestCase):

    def setUp(self):

        self.url_create = reverse('user_create')
        self.url_authenticate = reverse('user_authenticate')


    def make_user(self, username):

        data = {
            'username': username,
            'email': f'{username}@email.com'
        }

        response = self.client.post(
            self.url_create,
            data,
            format='json'
        )

        return response

    def test_post_user_valid(self):

        response = self.make_user("tester_create")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertIn(
            'username',
            response.data
        )

        self.assertIn(
            'password',
            response.data
        )

        self.assertIn(
            'token',
            response.data,
        )

    def test_post_authenticate(self):

        username = 'tester_auth'

        created = self.make_user('tester_auth')

        data = {
            'username': username,
            'password': created.data.get('password')
        }

        response = self.client.post(
            self.url_authenticate,
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            'token',
            response.data
        )
