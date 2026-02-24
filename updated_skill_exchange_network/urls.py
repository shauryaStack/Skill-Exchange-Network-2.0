"""
urls.py (project-level) — Root URL Configuration

This is the top-level URL router. It delegates:
    - /admin/  → Django's built-in admin panel
    - Everything else → core app's urls.py (core/urls.py)

The include('core.urls') line means all URLs defined in core/urls.py
are available at the root level (no prefix like /core/).
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # Django admin panel at /admin/
    path('', include('core.urls')),         # All app URLs at root level
]
