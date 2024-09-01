"""
Defines views and functions for a Django polling application,
including displaying, voting, and retrieving results for questions.
"""

from django.db.models import F
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    Display the last five published questions.

    This view renders a template named "polls/index.html" and provides
    a context variable named "latest_question_list" containing the last
    five published questions that are not scheduled for future publication.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions, excluding future ones.

        Questions are filtered by publication date, ensuring that only
        those published up to the current time are displayed, and are
        ordered by publication date in descending order.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    Display the details of a poll.

    This view renders a template named "polls/detail.html" and shows
    the details of a specific poll,
    excluding questions that are not yet published.
    """

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Exclude questions that aren't published yet.

        This method filters out questions that have a future publication date.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for poll details.

        If the poll is not published or is closed, redirect to the index page
        with an appropriate error message.
        """
        try:
            selected_question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request, "Question does not exist.")
            return redirect("polls:index")
        # Check if the question is published
        if not selected_question.is_published():
            messages.error(request, "Question is not published.")
            return redirect("polls:index")
        # Check if the question can be voted on
        if not selected_question.can_vote():
            messages.error(request, "Question is closed.")
            return redirect("polls:index")
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """
    Display the results of a poll.

    This view renders a template named "polls/results.html" and shows the
    results of a specific poll, ensuring that only published questions
    are displayed.
    """

    model = Question
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for poll results.

        If the poll is not published, redirect to the index page with an
        appropriate error message.
        """
        try:
            selected_question = self.get_queryset().get(pk=kwargs["pk"])
        except Question.DoesNotExist:
            messages.error(request, "Question does not exist.")
            return redirect("polls:index")

            # Check if the question is published
        if not selected_question.is_published():
            messages.error(request, "This question is not yet published.")
            return redirect("polls:index")
        return super().get(request, *args, **kwargs)


def vote(request, question_id):
    """
    Handle user votes in a Django application.

    This function processes the user's vote for a specific choice in a poll.
    It ensures that the user hasn't already voted and updates the vote count
    accordingly. If the user has already voted or hasn't selected a choice,
    an error message is displayed.
    """
    question = get_object_or_404(Question, pk=question_id)

    # Check if user has already voted per poll
    if request.session.get(f'has_voted_{question_id}', False):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You have already voted.",
            },
        )

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

        # mark this user as having voted
        request.session[f'has_voted_{question_id}'] = True

        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,)))
