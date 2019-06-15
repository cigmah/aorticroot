from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from questions.models import *
from choices.models import Choice
from tags.models import Tag


class QuestionTest(APITestCase):

    def setUp(self):
        self.initial_correct_choice = Choice.objects.create(
            content="correct choice",
            category=1
        )
        self.initial_incorrect_choice = Choice.objects.create(
            content="incorrect choice",
            category=1
        )
        self.initial_tag = Tag.objects.create(
            content="test tag",
            category=1
        )
        self.second_tag = Tag.objects.create(
            content="test tag 2",
            category=2
        )
        self.initial_question = Question.objects.create(
            stem="test stem",
            answer=self.initial_correct_choice,
            explanation="test explanation",
            user_id=None,
        )

        self.initial_user_data =  {
            'username': 'testQuestion',
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

    def testGetQuestion(self):
        url = reverse("question")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetQuestionId(self):
        url = reverse("question_id", args=[self.initial_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.initial_question.id)

    def makeBasePostQuestionData(self):
        data = {
            "stem": "test stem",
            "answer": {
                "content": "test answer",
                "category": 1
            },
            "explanation": "test explanation",
            "tags": [
                {
                    "content": "test new tag",
                    "category": 0,
                },
                {
                    "content": "test new tag 2",
                    "category": 1,
                }
            ],
            "distractors": [
                {
                    "content": "test distractor",
                    "category": 0
                },
                {
                    "content": "test distractor 2",
                    "category": 0
                },
            ],
        }
        return data


    def testPostQuestionWithNewDataWithAuth(self):
        url = reverse("question")
        data = self.makeBasePostQuestionData()
        response = self.authClient.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testPostQuestionWithOldTags(self):
        url = reverse("question")
        data = self.makeBasePostQuestionData()

        data['answer'] = {
            "content": self.initial_correct_choice.content,
            "category": self.initial_correct_choice.category,
        }

        data['distractors'] = [
            {
                "content": self.initial_incorrect_choice.content,
                "category": self.initial_incorrect_choice.category,
            }
        ]

        data['tags'] = [
            {
                "content": self.initial_tag.content,
                "category": self.initial_tag.category,
            },
            {
                "content": self.second_tag.content,
                "category": self.second_tag.category,
            }

        ]

        response = self.authClient.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testPostQuestionWithoutAuth(self):
        url = reverse('question')
        data = self.makeBasePostQuestionData()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostQuestionResponseCorrect(self):
        url = reverse('question_response')
        data = {
            'question_id': self.initial_question.id,
            'choice_id': self.initial_correct_choice.id,
        }
        response = self.authClient.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('correct'), True)

    def testPostQuestionResponseIncorrect(self):
        url = reverse('question_response')
        data = {
            'question_id': self.initial_question.id,
            'choice_id': self.initial_incorrect_choice.id,
        }
        response = self.authClient.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('correct'), False)

    def testPostQuestionComment(self):
        url = reverse('question_comment')
        data = {
            'question_id': self.initial_question.id,
            'content': 'test comment',
        }
        response = self.authClient.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
