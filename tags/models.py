from django.db import models

class Tag(models.Model):

    CATEGORIES = (
        (0, 'uncategorised'),
        (1, 'yearLevel'),
        (2, 'specialty'),
        (3, 'collection'),
        (4, 'domain'),
        (5, 'matrix'),
    )

    def __str__(self):
        return self.content
   
    content = models.CharField(max_length=80, unique=True)
    category = models.IntegerField(choices=CATEGORIES)

    class Meta:
        ordering = ('category', 'content',)
