from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    
    def __str__(self):
        return self.title
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
