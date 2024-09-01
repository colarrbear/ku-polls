"""Unit tests for the polls app."""
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_unpublished_question(self):
        """
        #1 is_published test for question with future pub date
        (question should not be shown in the UI)
        `is_published()` should return False when the pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_question(self):
        """
        #2 is_published test for question with the default pub date (now)
        `is_published()` should return True when the pub_date is in the past.
        """
        new_question = Question()
        self.assertTrue(new_question.is_published())

    def test_is_published_in_the_past(self):
        """
        #3 is_published test for question with past (already) pub date
        `is_published()` should return True when the pub_date is in the past.
        """
        time = timezone.now() - datetime.timedelta(days=3)
        old_question = Question(pub_date=time)
        self.assertTrue(old_question.is_published())

    def test_can_vote_published_question(self):
        """
        #1 can_vote test for published question [no end date]
        `can_vote()` should return True when the question is published.
        """
        time = timezone.now() - datetime.timedelta(days=3)
        question = Question(pub_date=time)
        self.assertTrue(question.can_vote())

    def test_can_vote_published_question_with_end_date(self):
        """
        #2 can_vote test for published question with end date
        `can_vote()` should return True when the question is published
        and the current date is before the end date.
        """
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date=pub_time, end_date=end_date)
        self.assertTrue(question.can_vote())

    def test_can_vote_published_question_after_end_date(self):
        """
        #3 can_vote test for published question with end date
        `can_vote()` should return False when the end date has passed.
        """
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time, end_date=end_date)
        self.assertFalse(question.can_vote())

    def test_can_vote_unpublished_question(self):
        """
        #4 can_vote test for unpublished question
        `can_vote()` should return False when the question is not published.
        """
        time = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date=time)
        self.assertFalse(question.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 not found.
        """
        future_question = create_question(question_text="Future question.",
                                          days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.",
                                        days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
