#!/usr/bin/env python
"""
manage.py — Django's Command-Line Utility

This is the entry point for all Django management commands:
    - python manage.py runserver       → Start the development server
    - python manage.py makemigrations  → Create database migration files
    - python manage.py migrate         → Apply migrations to the database
    - python manage.py createsuperuser → Create an admin account
    - python manage.py collectstatic   → Gather static files for production

You should never need to edit this file.
"""

import os
import sys


def main():
    # Tell Django which settings file to use
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'updated_skill_exchange_network.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not installed") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
