from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from posts.models import Post
from django.contrib.auth.models import User


class PostTest(APITestCase):

    
    def setUp(self):
        self.initial_user_data =  {
            'username': 'testPost',
            'password': 'tester'
        }

        self.initial_user = User.objects.create_user(
            username=self.initial_user_data.get('username'),
            password=self.initial_user_data.get('password')
        )

        token_response = self.client.post(reverse('user_authenticate'), self.initial_user_data, format='json')
        self.assertIn('token', token_response.data)
        self.initial_token = token_response.data.get('token')

        self.authClient = APIClient()
        self.authClient.credentials(HTTP_AUTHORIZATION='Token ' + self.initial_token)

    def addPost(self):
        url = reverse("post")
        data = {
            "title": "test title",
            "content": "test post",
        }
        response = self.authClient.post(url, data, format='json')
        return response

    def testAddPost(self):
        response = self.addPost()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGetPostList(self):
        self.addPost()
        self.addPost()
        self.addPost()
        url = reverse("post")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
