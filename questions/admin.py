from django.contrib import admin
from questions.models import *

admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(QuestionLike)
admin.site.register(QuestionTag)
admin.site.register(QuestionDistractor)
