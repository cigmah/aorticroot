from django.urls import path
from notes.views import *

urlpatterns = [
    path(
        "",
        NoteList.as_view(),
        name="note_list",
    ),
    path(
        "<int:pk>/",
        NoteRetrieveUpdateDestroy.as_view(),
        name="note_retrieve_update_destroy",
    ),
    path(
        "comments/",
        NoteCommentCreate.as_view(),
        name="notecomment_create",
    ),
]
