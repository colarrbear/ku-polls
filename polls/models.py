"""The above code defines Django models for a Question and
Choice with related fields and methods."""
from django.db import models
from django.utils import timezone
from django.contrib import admin

import datetime


class Question(models.Model):
    """
    Defines a model with a question text and publication date, along with a
    method to check if the question was published recently.

    attribute `question_text` Text of the question.
    attribute `pub_date` Date the question was published.
    attribute `end_date` Date the question will end.
        If null, can be voted on indefinitely.
    method `was_published_recently` A method to check if the question was
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=False)
    end_date = models.DateTimeField("date ended", auto_now_add=False,
                                    null=True, blank=True, default=None)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """
        return: The `was_published_recently` method returns a boolean value
        indicating whether the `pub_date` of the question falls within
        the last 24 hours from the current time.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """
        return: The `__str__` method returns the question text.
        """
        return self.question_text

    def is_published(self):
        """
        return: The `is_published` method returns a boolean value
        indicating whether the `pub_date` of the question is in the past.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """
        returns True if voting is allowed for this question.
        That means, the current date/time is between the pub_date and end_date.
        If end_date is null then can vote anytime after pub_date.
        """
        now = timezone.now()
        if not self.is_published():
            return False
        if self.end_date is None or self.end_date >= now:
            return True
        return False


class Choice(models.Model):
    """
    Defines a model with a choice text, the number of votes,
    and a foreign key to a question.

    attribute `question` The question the choice is associated with.
    attribute `choice_text` Text of the choice.
    attribute `votes` Number of votes for the choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        The `__str__` method returns the choice text.
        """
        return self.choice_text
