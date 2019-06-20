from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mail.models import *

class MailTest(APITestCase):

    def setUp(self):
        self.url_create = reverse('mail_create')

    def test_mail_create_bare_minimum(self):
        """
        A mail created with only a subject and content should be accepted.
        """

        data = {
            'subject': 'test subject',
            'content': 'test content',
        }

        response = self.client.post(self.url_create, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_create_full_info(self):
        """
        A mail created with full information should be accepted.
        """

        data = {
            'name': 'test name',
            'email': 'test@email.com',
            'subject': 'test subject',
            'content': 'test content',
        }

        response = self.client.post(self.url_create, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_create_incomplete(self):
        """
        Submitting a mail without a subject and/or content should fail.
        """

        data = {
            'subject': 'test subject',
        }

        response = self.client.post(self.url_create, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
