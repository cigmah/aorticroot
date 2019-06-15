from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import *


class UserTest(APITestCase):

    def makeUser(self, username):
        url = reverse("user")
        data = {
            "username": username,
        }
        response = self.client.post(url, data, format='json')
        return response

    def testPostUserValid(self):
        response = self.makeUser("tester")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        self.assertIn('token', response.data, )

    def testPostAuthenticate(self):
        username = 'testerAuth'
        created = self.makeUser('testerAuth')
        url = reverse("user_authenticate")
        data = {
            'username': username,
            'password': created.data.get('password')
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
