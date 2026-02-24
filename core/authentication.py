"""
authentication.py — Firebase Token Authentication for REST API

This file provides a custom authentication backend for Django REST Framework.
When mobile/frontend apps send a Firebase ID token in the Authorization header,
this class verifies it with Firebase and finds (or creates) the matching Django user.

How it works:
    1. Client sends: Authorization: Bearer <firebase_id_token>
    2. This class intercepts the request (DRF calls authenticate())
    3. We verify the token with Firebase Admin SDK
    4. If valid, we find/create a Django User linked to that Firebase UID
    5. DRF then treats the request as authenticated

Configuration:
    - FIREBASE_SERVICE_ACCOUNT in settings.py must contain the Firebase credentials
    - If left as empty dict {}, Firebase auth is skipped (runs in local-only mode)
"""

import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import User

# Initialize Firebase Admin SDK once when the module loads.
# The check for `firebase_admin._apps` prevents re-initialization on hot-reloads.
if settings.FIREBASE_SERVICE_ACCOUNT and not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Custom DRF authentication class that validates Firebase ID tokens.

    Returns:
        (user, None) if authentication succeeds
        None if no Bearer token is present (lets other backends try)
        Raises AuthenticationFailed if the token is invalid
    """

    def authenticate(self, request):
        # If Firebase isn't configured, skip this backend entirely
        if not settings.FIREBASE_SERVICE_ACCOUNT:
            return None

        # Extract the Authorization header (format: "Bearer <token>")
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        parts = auth_header.split()

        # If the header doesn't look like "Bearer <token>", skip
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        token = parts[1]

        try:
            # Verify the Firebase ID token — this calls Firebase servers
            decoded = firebase_auth.verify_id_token(token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Firebase token")

        # Extract user info from the decoded token
        firebase_uid = decoded["uid"]
        email = decoded.get("email", "")

        # Find existing user by Firebase UID, or create a new one
        # get_or_create returns (user, was_created_bool)
        user, _ = User.objects.get_or_create(
            firebase_uid=firebase_uid,
            defaults={"username": email or firebase_uid, "email": email},
        )

        return (user, None)
