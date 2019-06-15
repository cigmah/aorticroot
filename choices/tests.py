from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from choices.models import *


class ChoiceTest(APITestCase):

    def addChoice(self):
        url = reverse("choice")
        data = {
            "content": "test choice",
            "category": 1
        }
        response = self.client.post(url, data, format='json')
        return response

    def testAddChoice(self):
        response = self.addChoice()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGetChoice(self):
        added = self.addChoice()
        url = reverse("choice_id", args=[added.data['id']])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], added.data['id'])
