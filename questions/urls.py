""" URLs for Question views.

These URLs are subrouted under "questions/".

"""

from django.urls import path
from questions.views import *

urlpatterns = [
    path(
        # questions/
        "",
        QuestionCreate.as_view(),
        name="question_create",
    ),
    path(
        # questions/
        "",
        QuestionList.as_view(),
        name="question_list",
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
        QuestionRetrieve.as_view(),
        name="question_retrieve",
    ),
    path(
        # questions/<int:pk>/
        "<int:pk>/",
        QuestionUpdate.as_view(),
        name="question_update",
    ),
    path(
        # questions/<int:pk>/
        "<int:pk>/",
        QuestionDestroy.as_view(),
        name="question_destroy",
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
