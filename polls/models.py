"""Contains the models for the Polls app."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Defines a model for questions in a poll.

    Attributes:
        question_text (str): Text of the question.
        pub_date (datetime): Date the question was published.
        end_date (datetime): Date the question will end. If null, can be voted
                             on indefinitely.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField(
        "date ended", auto_now_add=False, null=True, blank=True, default=None
    )

    @admin.display(
        boolean=True,
        ordering=["pub_date", "end_date"],
        description="Published recently?",
    )
    def was_published_recently(self):
        """Check if the question was published in the last 24 hours.

        Returns:
            bool: True if published within last 24 hours, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """Return the question text."""
        return self.question_text

    def is_published(self):
        """Check if the question is published.

        Returns:
            bool: True if published, False otherwise.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check if voting is allowed for this question.

        Returns:
            bool: True if voting is allowed, False otherwise.
        """
        now = timezone.now()
        if not self.is_published():
            return False
        if self.end_date is None or self.pub_date <= now <= self.end_date:
            return True
        return False


class Choice(models.Model):
    """Defines a model for choices in a poll.

    Attributes:
        question (Question): The question the choice is associated with.
        choice_text (str): Text of the choice.
        votes (int): Number of votes for the choice.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Return the votes for the choice."""
        return self.vote_set.count()
        # return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return the choice text."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
