"""This file is used to register the models with the admin site."""
from django.contrib import admin
from .models import Question, Choice

from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    """Class to customize the admin interface for the Question model."""
    fields = ["pub_date", "question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
