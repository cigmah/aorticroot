"""aorticroot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
import tags.views
import choices.views
import questions.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Tags
    path('tag/', tags.views.TagList.as_view()),
    path('tag/<int:pk>/', tags.views.TagDetail.as_view()),
    # Choices
    path('choice/', choices.views.ChoiceList.as_view()),
    path('choice/<int:pk>/', choices.views.ChoiceDetail.as_view()),
    # Questions
    path('question/', questions.views.QuestionList.as_view(), name="question_many"),
    path('question/<int:pk>/', questions.views.QuestionDetail.as_view(), name="question"),
    path('question/comment/', questions.views.QuestionCommentList.as_view()),
    path('question/comment/<int:pk>', questions.views.QuestionCommentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
