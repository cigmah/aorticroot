from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from questions.models import *
from choices.models import Choice


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
        self.initial_question = Question.objects.create(
            stem="test stem",
            answer=self.initial_correct_choice,
            explanation="test explanation",
            user_id=None,
        )

    def testGetQuestion(self):
        url = reverse("question")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetQuestionId(self):
        url = reverse("question_id", args=[self.initial_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.initial_question.id)
