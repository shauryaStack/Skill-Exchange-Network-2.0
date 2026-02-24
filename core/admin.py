"""
admin.py — Django Admin Panel Configuration

This file customizes how our models appear in Django's built-in admin panel
(accessible at /admin/). Each @admin.register decorator registers a model
and the class below it controls what columns are shown, what can be searched, etc.

To access the admin panel:
    1. Create a superuser: python manage.py createsuperuser
    2. Go to http://localhost:8000/admin/
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, UserTeaches, ExchangeRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Extends Django's built-in UserAdmin so our custom User model
    shows properly in the admin panel with our extra fields.
    """
    list_display = ('username', 'email', 'first_name', 'division', 'date_joined')
    list_filter = ('division', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin view for managing the skill catalog."""
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)  # Sidebar filter by category


@admin.register(UserTeaches)
class UserTeachesAdmin(admin.ModelAdmin):
    """Admin view for seeing which users teach which skills."""
    list_display = ('user', 'skill', 'available_time')
    list_filter = ('skill__category', 'available_time')  # Filter by skill's category
    search_fields = ('user__first_name', 'user__username', 'skill__name')


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    """Admin view for managing exchange requests and their statuses."""
    list_display = ('requester', 'receiver', 'skill', 'offering_skill', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('requester__first_name', 'receiver__first_name', 'skill__name')
    date_hierarchy = 'created_at'  # Adds date-based drill-down navigation at the top
