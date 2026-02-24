"""
apps.py — App Configuration

This file tells Django about our 'core' app.
Django reads this to register the app in INSTALLED_APPS (settings.py).
Without this, Django won't discover our models, views, or templates.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    # Use BigAutoField for auto-generated primary keys (supports larger IDs)
    default_auto_field = 'django.db.models.BigAutoField'

    # Must match the app directory name and the entry in INSTALLED_APPS
    name = 'core'

    # Human-readable name shown in the Django admin panel
    verbose_name = 'Core App'
