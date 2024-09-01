"""Apps configuration for the `polls` application."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """`polls` application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
