from django.db import models


class Mail(models.Model):

    name = models.CharField(max_length=80, null=True, blank=True)

    subject = models.CharField(max_length=80)

    email = models.EmailField(null=True, blank=True)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
