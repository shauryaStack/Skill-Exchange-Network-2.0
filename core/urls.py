"""
urls.py (core app) — URL Routing

Maps URL paths to view functions. When someone visits a URL,
Django checks this list top-to-bottom and calls the matching view.

URL patterns are organized into sections:
    - Regular pages (HTML views)
    - Firebase authentication endpoint
    - API routes (JSON endpoints for AJAX/mobile)

The 'name' parameter lets us reference URLs in templates and code
using {% url 'name' %} instead of hardcoding paths.
"""

from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # --- Page Views (return HTML) ---
    path('', views.index, name='index'),                         # Home page
    path('register/', views.register_view, name='register'),     # Registration form
    path('login/', views.login_view, name='login'),              # Login form
    path('logout/', views.logout_view, name='logout'),           # Logout action
    path('profile/', views.profile_view, name='profile'),        # User dashboard
    path('browse/', views.browse_view, name='browse'),           # Browse all skills
    path('match/', views.match_view, name='match'),              # Find teachers for a skill
    path('sessions/', views.sessions_view, name='sessions'),     # View learning sessions

    # --- Exchange Request Actions (form POST handlers) ---
    path('request-exchange/', views.request_exchange, name='request_exchange'),
    path('accept-exchange/<int:exchange_id>/', views.accept_exchange, name='accept_exchange'),
    path('reject-exchange/<int:exchange_id>/', views.reject_exchange, name='reject_exchange'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('remove-skill/<int:teach_id>/', views.remove_skill, name='remove_skill'),

    # --- Session Management ---
    path('reschedule-session/', views.reschedule_session, name='reschedule_session'),
    path('save-meeting-link/', views.save_meeting_link, name='save_meeting_link'),
    path('send-notification/', views.send_notification, name='send_notification'),

    # --- Firebase Authentication ---
    path('firebase-login/', views.firebase_login, name='firebase_login'),

    # --- API Routes (return JSON for AJAX/mobile) ---
    path('api/request-exchange/', api_views.api_request_exchange, name='api_request_exchange'),
    path('api/notifications/', api_views.api_notifications, name='api_notifications'),
    path('api/health/', api_views.api_health, name='api_health'),
    path('api/live-users/', api_views.api_live_users, name='api_live_users'),
    path('api/exchanges/<int:exchange_id>/schedule/', api_views.api_schedule_session, name='api_schedule_session'),
]
