from django.urls import path
from mail.views import *

urlpatterns = [
    path(
        '',
         MailCreate.as_view(),
        name='mail_create'
    )
]
