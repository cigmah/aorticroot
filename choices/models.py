from django.db import models

class Choice(models.Model):

    CATEGORIES = (
        (0, 'uncategorised'),
        (1, 'symptom'),
        (2, 'sign'),
        (3, 'diagnosis'),
        (4, 'investigation'),
        (5, 'medication'),
        (6, 'intervention'),
        (7, 'pathogen'),
        (8, 'vaccine'),
    )

    def __str__(self):
        return self.content

    content = models.TextField(unique=True)
    category = models.IntegerField(choices=CATEGORIES)

    class Meta:
        ordering = ('category', 'content')
