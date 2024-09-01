"""Apps configuration for the `polls` application."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    The `PollsConfig` class in the Django application `polls`
    sets the default auto field to `BigAutoField`.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
