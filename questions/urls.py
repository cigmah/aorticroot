""" URLs for Question views.

These URLs are subrouted under "questions/".

"""

from django.urls import path
from questions.views import *

urlpatterns = [
    path(
        # questions/
        "",
        QuestionListCreate.as_view(),
        name="question_list_create",
    ),
    path(
        # questions/test/
        "test/",
        QuestionIdList.as_view(),
        name="question_test",
    ),
    path(
        # questions/<int:pk>/
        "<int:pk>/",
        QuestionRetrieveUpdateDestroy.as_view(),
        name="question_retrieve_update_destroy",
    ),
    path(
        # questions/ratings/
        "ratings/",
        QuestionRatingCreate.as_view(),
        name="question_rating_create",
    ),
    path(
        # questions/comments/
        "comments/",
        QuestionCommentCreate.as_view(),
        name="question_comment_create",
    ),
    path(
        # questions/responses/
        "responses/",
        QuestionResponseListCreate.as_view(),
        name="question_response_list_create",
    ),
    path(
        # questions/accuracy/
        "accuracy/",
        QuestionAccuracyRetrieve.as_view(),
        name="question_accuracy_retrieve",
    ),
]
