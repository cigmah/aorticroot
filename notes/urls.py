from django.urls import path
from notes.views import *

urlpatterns = [
    path(
        '',
         NoteListCreate.as_view(),
        name='note_list_create',
    ),
    path(
        '<int:pk>/',
        NoteRetrieveUpdateDestroy.as_view(),
        name='note_retrieve_update_destroy',
    ),
    path(
        'comments/',
        NoteCommentCreate.as_view(),
        name='notecomment_create',
    )
]
