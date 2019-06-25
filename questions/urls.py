from django.urls import path
from questions.views import *

urlpatterns = [
    path(
        "",
        QuestionListCreate.as_view(),
        name="question_list_create",
    ),
    path(
        "random/",
        QuestionRandom.as_view(),
        name="question_random",
    ),
    path(
        "<int:pk>/",
        QuestionRetrieveUpdateDestroy.as_view(),
        name="question_retrieve_update_destroy",
    ),
    path(
        "responses/",
        QuestionResponseCreate.as_view(),
        name="question_response_create",
    ),
    path(
        "likes/",
        QuestionLikeCreate.as_view(),
        name="question_like_create",
    ),
    path(
        "flags/",
        QuestionFlagCreate.as_view(),
        name="question_flag_create",
    ),
    path(
        "comments/",
        QuestionCommentCreate.as_view(),
        name="question_comment_create",
    )
]
