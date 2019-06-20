from django.contrib import admin
from notes.models import *

admin.site.register(Note)
admin.site.register(NoteComment)

# Register your models here.
