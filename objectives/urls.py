""" URLs for objectives views. 

These URLs are stored subrouted under "objectives/"
"""
from django.urls import path
from objectives.views import ObjectiveListCreate, ObjectiveRetrieveUpdateDestroy

urlpatterns = [
    path(
        # objectives/
        "",
        ObjectiveListCreate.as_view(),
        name="objective_list_create"
    ),
    path(
        # /objectives/<int:pk>
        "<int:pk>/",
        ObjectiveRetrieveUpdateDestroy.as_view(),
        name="objective_retrieve_update_destroy"
    ),
]
