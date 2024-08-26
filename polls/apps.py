"""The `PollsConfig` class is a Django application configuration class for the `polls` app with a
default auto field set to `BigAutoField`."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """The `PollsConfig` class in the Django application `polls`
    sets the default auto field to `BigAutoField`."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
