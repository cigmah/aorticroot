from django.contrib import admin
from questions.models import *

admin.site.register(Question)
admin.site.register(QuestionChoice)
admin.site.register(QuestionResponse)
admin.site.register(QuestionLike)
admin.site.register(QuestionFlag)
