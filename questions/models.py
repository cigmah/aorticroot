""" Models relating to multiple choice questions.
"""
from django.db import models
from django.contrib.auth.models import User
from objectives.models import Objective


class Question(models.Model):
    """ A Question contains a basic multiple-choice question.

    Each Question must be attached to a parent Objective. The multiple-choice options
    for each question are stored in a separate table, QuestionChoice, so that questions
    can have a flexible number of options. 
    """

    objective = models.ForeignKey(
        Objective, 
        on_delete=models.PROTECT, 
        related_name="objective_question",
        help_text="The parent learning objective for this question."
    )
    contributor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_question",
        help_text="The user who contributed this question."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time of creation."
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        help_text="Time of modification."
    )
    stem = models.TextField(
        help_text="The basic question stem."
    )

    def __str__(self):
        return self.stem


class QuestionChoice(models.Model):
    """ QuestionChoice contain the choices for each question.

    This is modelled as a one-to-many relation, with the parent
    question identified through a foreign key.

    Each question should only have one correct choice (i.e. there
    should only be one choice with `is_correct=True` for each question.
    It doesn't seem this can be enforced at the model layer, so this
    should be enforced through the application logic.
    """

    question = models.ForeignKey(
        Question, 
        related_name="question_choice",
        on_delete=models.CASCADE,
        help_text="The parent question to which this choice belongs."
    )
    content = models.TextField(
        help_text="The text displayed for this choice under a question."
    )
    explanation = models.TextField(
        help_text="The explanation for why this chocie is right or wrong."
    )
    is_correct = models.BooleanField(
        help_text="Whether this is the correct choice, or an incorrect choice."
    )

    class Meta:
        # Each choice for a question must be different
        unique_together = ("question", "content")

    def __str__(self):
        return self.content


class QuestionResponse(models.Model):
    """ QuestionResponse contains a user's choice response to a question.

    Every time a user attempts a question, their choice will be saved as a 
    QuestionResponse object. 

    The choices will save anonymous responses as well, so the user field is optional.

    The question need not be saved in this model, as every choice is attached to the
    parent question anyway. 
    """

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_response",
        help_text="Optional user who sent the response. If null, assume to be anonymous."
    )
    choice = models.ForeignKey(
        QuestionChoice,
        on_delete=models.CASCADE,
        related_name="choice_response",
        help_text="The choice which was selected for this response."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The time the response was submitted."
    )

    def __str__(self):
        return f"{self.user} chose '{self.choice}' @ {self.created_at}"


class QuestionRating(models.Model):
    """ QuestionRating contain ratings from users for a question.

    Anyone can rate questions a rating out of 5 stars. They do not need to be 
    authenticated. If they are authenticated, they can only rate the question
    once. 
    """

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The user who rated the question."
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="question_rating",
        help_text="The question that was rated"
    )
    rating = models.IntegerField(
        help_text="An integer rating in the range 1-5 inclusive."
    )

    def __str__(self):
        return f"{self.user} rated Question #{self.question.id} {self.rating}/5 stars."


class QuestionComment(models.Model):
    """ QuestionComment contains comments that users can add to questions.

    Comments can be posted anonymously.
    """

    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name="question_comment",
        help_text="The question that was commented on."
    )
    contributor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The optional user who authored the comment. If null, it is anonymous."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The time the comment was posted."
    )
    content = models.TextField(
        help_text="The comment iself, stored as Markdown."
    )

    def __str__(self):
        return self.content
