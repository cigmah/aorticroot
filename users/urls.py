from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import *

urlpatterns = [
    path("", UserCreate.as_view(), name="user_create"),
    path("authenticate/", Authenticate.as_view(), name="user_authenticate"),
]
