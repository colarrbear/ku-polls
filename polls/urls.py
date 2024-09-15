"""Urls path for the `polls` app."""

from django.urls import path, re_path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('signup/', views.signup, name='signup'),
    # Catch-all for non-integer pk values
    re_path(r"^(?![\d]+/$).*$", views.IndexView.as_view(),
            name="index_redirect"),

]
