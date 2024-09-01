"""Unit tests for the polls app."""
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    """Tests for the Question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for future questions."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for old questions."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Returns True for recent questions."""
        time = (timezone.now() -
                datetime.timedelta(hours=23, minutes=59, seconds=59))
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_unpublished_question(self):
        """is_published() returns False for future questions."""
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_question(self):
        """is_published() returns True for questions with default pub_date."""
        new_question = Question()
        self.assertTrue(new_question.is_published())

    def test_is_published_in_the_past(self):
        """is_published() returns True for questions with past pub_date."""
        time = timezone.now() - datetime.timedelta(days=3)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_can_vote_published_question(self):
        """can_vote() returns True for published questions with no end date."""
        time = timezone.now() - datetime.timedelta(days=3)
        question = Question(pub_date=time)
        self.assertTrue(question.can_vote())

    def test_can_vote_published_question_with_end_date(self):
        """can_vote() returns True for published questions before end date."""
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date=pub_time, end_date=end_date)
        self.assertTrue(question.can_vote())

    def test_can_vote_published_question_after_end_date(self):
        """can_vote() returns False for questions past end date."""
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time, end_date=end_date)
        self.assertFalse(question.can_vote())

    def test_can_vote_unpublished_question(self):
        """can_vote() returns False for unpublished questions."""
        time = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date=time)
        self.assertFalse(question.can_vote())

    def test_can_vote_default_published_date(self):
        """can_vote() returns True for questions with default pub_date."""
        question = Question()
        self.assertTrue(question.can_vote())


def create_question(question_text, days):
    """Create a question with given text published given days offset."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """Tests for the index view of questions."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Questions with pub_date in the past are displayed on index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """Questions with future pub_date not displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """Only past questions are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """The index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """Tests for the detail view of questions."""

    def test_future_question(self):
        """The detail view of a future question redirects to the index page."""
        future_question = (create_question
                           (question_text="Future question.", days=5))
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a past question displays the question's text."""
        past_question = (create_question
                         (question_text="Past Question.", days=-5))
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
