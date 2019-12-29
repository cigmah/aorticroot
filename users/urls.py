""" URLs for user views.

These URLs are stored subrouted under "users/"

"""
from django.urls import path
from users.views import UserCreate, Authenticate

urlpatterns = [
    path(
        # users/
        "",
        UserCreate.as_view(),
        name="user_create"
    ),
    path(
        # users/authenticate/
        "authenticate/",
        Authenticate.as_view(),
        name="user_authenticate"
    ),
]
