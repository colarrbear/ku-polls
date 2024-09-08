"""Define views for the polls app."""

from django.db.models import F
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Display five most recent polls."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """Display the choices for a poll and allow voting."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        If poll is not published or closed, redirect to index page.

        https://docs.djangoproject.com/en/5.1/ref/class-based-views/base/
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
        # Render the page
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """Result view displays the results of a poll."""

    model = Question
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs):
        """Get the question and check if it is published."""
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

@login_required
def vote(request, question_id):
    """Handle user votes in a Django application."""
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, "This question is not published yet.")
        return HttpResponseRedirect(reverse("polls:index"))

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            }
        )

    # Reference to the current user
    this_user = request.user

    # Get the user's vote
    try:
        # vote = this_user.vote_set.get(choice__question=question)
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # user has a vote for this question! update his choice.
        vote.choice = selected_choice
        vote.save()
        messages.success(request, "Your vote has been updated.")
    except Vote.DoesNotExist:
        # does not have a vote yet, create a new one
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
        vote.save()
        # automatically saved
        messages.success(request, "Your vote has been recorded.")

    # if the user has a vote for this question:
    #     change the vote in his vote
    #     save the vote
    # else:
    # doesn't have a vote for this question
    #     create a new vote

    return HttpResponseRedirect(
        reverse("polls:results", args=(question.id,))
    )
