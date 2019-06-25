from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from notes.models import Note
from datetime import timedelta



class Question(models.Model):
    """
    This module contains multiple-choice questions which are attached
    to parent notes. Each question MUST have a parent note.
    """
    
    # Domain constants relating to specific subclassification
    # of notes - either foundation knowledge for practice, or
    # relating to specific tasks of clinical practice.
    GENERAL_DOMAIN = 0
    FOUNDATION     = 1
    ASSESSMENT     = 2
    INVESTIGATION  = 3
    DIAGNOSIS      = 4
    MANAGEMENT     = 5

    # Domain choices.
    DOMAIN_CHOICES = [
        (GENERAL_DOMAIN , "GENERAL_DOMAIN"),
        (FOUNDATION     , "FOUNDATION"),
        (ASSESSMENT     , "ASSESSMENT"),
        (INVESTIGATION  , "INVESTIGATION"),
        (DIAGNOSIS      , "DIAGNOSIS"),
        (MANAGEMENT     , "MANAGEMENT"),
    ]

    note = models.ForeignKey(
        Note,
        on_delete=models.PROTECT,
        related_name='note_question',
    )

    contributor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    domain = models.IntegerField(
        choices=DOMAIN_CHOICES,
        default=GENERAL_DOMAIN
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    stem = models.TextField()

    def __str__(self):
        return self.stem


class QuestionChoice(models.Model):
    """
    This module contains the multiple choice options for each
    question, as a one-to-many relation.
    """

    question = models.ForeignKey(
        Question,
        related_name="question_choice",
        on_delete=models.CASCADE,
    )

    content = models.CharField(
        max_length=80
    )

    explanation = models.TextField(
        null=True
    )

    # Enforcing that there is exactly one is_correct=True
    # row per QuestionChoice will have to be done on the
    # application layer. Initially, the answer and explanation
    # were put into the Question table to guarantee one and only
    # one correct answer, but this complicated the application
    # logic somewhat, and it was deemed easier to enforce this
    # both on the frontend and during the serialization of
    # received POST data rather than on the database model
    # level.
    # Question choices should only ever be created as a batch.
    is_correct = models.BooleanField()

    class Meta:
        # Ensure each choice for a question is different
        unique_together = ("question", "content")

    def __str__(self):
        return self.content


class QuestionResponse(models.Model):
    """
    This model contains responses that users give when they
    answer questions.

    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_response',
    )

    choice = models.ForeignKey(
        QuestionChoice,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    ease = models.FloatField(
        default=2.5
    )

    interval_days = models.FloatField(
        default=1
    )

    next_due_datetime = models.DateTimeField(
        default=timezone.now() + timedelta(days=1)
    )

    def __str__(self):
        return f"{self.question_id}--{self.user_id}"


class QuestionLike(models.Model):
    """
    This model contains likes from users who express positivity
    about a question.
    """

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user_id}--{self.question_id}"


class QuestionFlag(models.Model):
    """
    This model contains flgs from users who express negativity
    about a question.

    Generally, this should not be exposed via an API; instead,
    the aggregate should be counted and tallied for responses.

    Alternatively, flagged questions can simply not be shown.
    """

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user_id}--{self.question_id}"


class QuestionComment(models.Model):
    """
    This model contains comments that users can add to questions.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    content = models.TextField()

    def __str__(self):
        return self.content
