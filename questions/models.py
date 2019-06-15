from django.db import models
from django.db import models
from tags.models import Tag
from choices.models import Choice
from django.contrib.auth.models import User


class Question(models.Model):

    def __str__(self):
        return self.stem

    stem = models.TextField()
    answer = models.ForeignKey(Choice, on_delete=models.PROTECT)
    explanation = models.TextField()
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    flagged = models.BooleanField(default=False)

class QuestionTag(models.Model):

    def __str__(self):
        return f'{self.question_id}-{self.tag_id}'

    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='tags')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question_id', 'tag_id')

class QuestionDistractor(models.Model):

    def __str__(self):
        return f'{self.question_id}--{self.choice_id}'

    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='distractors')
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question_id', 'choice_id')

class QuestionComment(models.Model):

    def __str__(self):
        return self.content

    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class QuestionLike(models.Model):

    def __str__(self):
        return f'{self.user_id}--{self.question_id}'

    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user_id', 'question_id')
