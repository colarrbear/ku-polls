"""
Defines views and functions for a Django polling application,
including displaying, voting, and getting results for questions.
"""

from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    The `IndexView` class is a generic ListView that displays
    the last five published questions in a template named "polls/index.html".
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions not including polls
        set to be published in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    This function retrieves questions that have been published
    based on the current time.
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    Defines a view for displaying poll results and a function for
    handling user votes in a Django application.
    """
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    A view function named `vote` in a Django polling application.
    This function is responsible for handling user votes on a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,)))
