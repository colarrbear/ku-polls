from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"),
#     # added the word 'specifics'
#     # path("specifics/<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/5/ -> question_id
#     path("<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/5/results/ -> question_id results
#     path("<int:question_id>/results/", views.results, name="results"),
#     # ex: /polls/5/vote/ -> question_id vote
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]
