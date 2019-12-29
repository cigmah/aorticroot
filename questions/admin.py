from django.contrib import admin
from questions.models import (
    Question,
    QuestionChoice,
    QuestionResponse,
    QuestionRating,
    QuestionComment,
)

admin.site.register(Question)
admin.site.register(QuestionChoice)
admin.site.register(QuestionResponse)
admin.site.register(QuestionRating)
admin.site.register(QuestionComment)
