"""The above code defines Django models for a Question and
Choice with related fields and methods."""
from django.db import models
from django.utils import timezone

import datetime


class Question(models.Model):
    """
    Defines a model with a question text and publication date, along with a
    method to check if the question was published recently.
    
    :return: The `was_published_recently` method is returning a boolean value
    indicating whether the `pub_date` of the question falls within
    the last 24 hours from the current time.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """
        return: The `__str__` method returns the question text.
        """
        return self.question_text

    def was_published_recently(self):
        """
        return: The `was_published_recently` method returns a boolean value
        indicating whether the `pub_date` of the question falls within
        the last 24 hours from the current time.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Defines a model with a choice text, the number of votes,
    and a foreign key to a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        return: The `__str__` method returns the choice text.
        """
        return self.choice_text
