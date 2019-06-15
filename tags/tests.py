from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from tags.models import *


class TagTest(APITestCase):

    def addTag(self):
        url = reverse("tag")
        data = {
            "content": "test tag",
            "category": 1
        }
        response = self.client.post(url, data, format='json')
        return response

    def testAddTag(self):
        response = self.addTag()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGetTag(self):
        added = self.addTag()
        url = reverse("tag_id", args=[added.data['id']])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], added.data['id'])
