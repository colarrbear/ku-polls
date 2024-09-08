"""Unit tod for the polls app."""
import datetime
import django.test

from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # to "login" a user using code
from mysite import settings
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question, Choice


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
        """was_published_recently() returns True for recent questions."""
        time = (timezone.now() - datetime.
                timedelta(hours=23, minutes=59, seconds=59))
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
    """Create poll with the given text and published the given days offset."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """Tests for the index view of questions."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertListEqual(
            list(response.context["latest_question_list"]),
            [],
        )

    def test_past_question(self):
        """Questions with a past pub_date are displayed on index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertListEqual(
            list(response.context["latest_question_list"]),
            [question],
        )

    def test_future_question(self):
        """Questions with a future pub_date aren't displayed on index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertListEqual(list(response.context["latest_question_list"]),
                             [])

    def test_future_question_and_past_question(self):
        """Only past questions are displayed if both past and future exist."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertListEqual(
            list(response.context["latest_question_list"]),
            [question],
        )

    def test_two_past_questions(self):
        """The index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertListEqual(
            list(response.context["latest_question_list"]),
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


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        #superclass setUp creates a Client object and initializes test database
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester"
        self.user1.save()
        # we need a poll question to test voting
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_logout(self):
        """A user can logout using the logout url.

        As an authenticated user,
        when I visit /accounts/logout/
        then I am logged out
        and then redirected to the login page.
        """
        logout_url = reverse("logout")
        # Authenticate the user.
        # We want to logout this user, so we need to associate the
        # user user with a session.  Setting client.user = ... doesn't work.
        # Use Client.login(username, password) to do that.
        # Client.login returns true on success
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        # visit the logout page
        form_data = {}
        response = self.client.post(logout_url, form_data)
        self.assertEqual(302, response.status_code)

        # should redirect us to the login page
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can login using the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using a POST request
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser",
                     "password": "FatChance!"
                     }
        response = self.client.post(login_url, form_data)
        # after successful login, should redirect browser somewhere
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Authentication is required to submit a vote.

        As an unauthenticated user,
        when I submit a vote for a question,
        then I am redirected to the login page
          or I receive a 403 response (FORBIDDEN)
        """
        vote_url = reverse('polls:vote', args=[self.question.id])

        # what choice to vote for?
        choice = self.question.choice_set.first()
        # the polls detail page has a form, each choice is identified by its id
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote_url, form_data)
        # should be redirected to the login page
        self.assertEqual(response.status_code, 302)  # could be 303
        # include reverse('login') does not include

        login_url = reverse('login')
        expected_url = f"{login_url}?next={vote_url}"
        self.assertEqual(response.url, expected_url)
        # the query parameter ?next=/polls/1/vote/
        # self.assertRedirects(response, reverse('login') )
        # How to fix it?
        # login_with_next = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, expected_url)

