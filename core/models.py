"""
models.py — Database Models for Skill Exchange Network

This file defines all the database tables (models) used in the app.
Django converts these Python classes into actual database tables.

Models defined here:
    - User: Extended user model with extra fields (division, phone, firebase)
    - Skill: Skills available for teaching/learning (e.g., Python, React)
    - UserTeaches: Links a user to a skill they can teach (many-to-many through table)
    - ExchangeRequest: A request from one user to another for a skill exchange
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extended user model — inherits Django's built-in user (username, email, password, etc.)
    and adds custom fields specific to our app.

    Why AbstractUser?
    - We get all of Django's auth features (login, logout, password hashing) for free
    - We can add our own fields on top (division, phone, firebase_uid)
    """

    # The department/division the user belongs to (e.g., "Computer Science")
    division = models.CharField(max_length=100, blank=True, null=True)

    # Phone number — used for WhatsApp notifications via Twilio
    phone = models.CharField(max_length=15, blank=True, null=True)

    # Firebase UID — links this Django user to their Firebase account
    # unique=True ensures no two Django users share the same Firebase account
    firebase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'core_user'           # Explicit table name in the database
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        # Display name priority: first_name > username > email
        return self.first_name or self.username or self.email


class Skill(models.Model):
    """
    Represents a skill that can be taught or learned.
    Skills are shared across all users (e.g., "Python Programming", "UI/UX Design").

    These are pre-seeded in the register_view when the database is empty.
    """

    name = models.CharField(max_length=100, unique=True)  # Skill name must be unique
    category = models.CharField(max_length=50)             # Groups skills (e.g., "Programming", "Design")
    created_at = models.DateTimeField(auto_now_add=True)   # Auto-set when created

    class Meta:
        ordering = ['name']              # Default alphabetical ordering
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name


class UserTeaches(models.Model):
    """
    Junction/through table — connects a User to a Skill they can teach.

    Why a separate model instead of ManyToManyField?
    - We need extra fields on the relationship (proficiency, available_time, notes)
    - A plain ManyToMany wouldn't let us store this extra data

    Example: "John teaches Python at Intermediate level, available on Weekends"
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userteaches')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='userteaches')

    # How skilled the user is at teaching this
    proficiency = models.CharField(
        max_length=20,
        default='intermediate',
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ]
    )

    available_time = models.CharField(max_length=100, default='Flexible')  # When the user is free to teach
    notes = models.TextField(blank=True, null=True, max_length=500)        # Optional notes about teaching style
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate entries — a user can only teach a specific skill once
        unique_together = ('user', 'skill')
        verbose_name_plural = "User Teaches"

    def __str__(self):
        return f"{self.user.first_name} teaches {self.skill.name} ({self.proficiency})"


class ExchangeRequest(models.Model):
    """
    Represents a skill exchange request between two users.

    Flow:
        1. User A (requester) sends a request to User B (receiver) for a skill
        2. User A offers to teach something in return (offering_skill)
        3. User B can accept or reject the request
        4. If accepted, they can schedule a meeting with date/time/link

    Status lifecycle: pending → accepted/rejected → completed
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    PLATFORM_CHOICES = [
        ('google_meet', 'Google Meet'),
        ('teams', 'Microsoft Teams'),
    ]

    # Who sent the request
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'  # Access via: user.sent_requests.all()
    )

    # Who received the request (the teacher)
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests'  # Access via: user.received_requests.all()
    )

    # The skill being requested to learn
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    # What the requester offers to teach in return (free text, not a FK)
    offering_skill = models.CharField(max_length=100, help_text="What the requester offers in exchange")

    preferred_time = models.CharField(max_length=50, default='Flexible')
    message = models.TextField(blank=True, null=True)  # Optional personal message
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # --- Meeting details (filled after the request is accepted) ---
    meeting_link = models.URLField(blank=True, null=True, help_text="Shared meeting link")
    meeting_platform = models.CharField(
        max_length=50, blank=True, null=True,
        choices=PLATFORM_CHOICES,
        help_text="Google Meet or Teams"
    )
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)

    # Timestamps — auto_now_add sets on creation, auto_now updates on every save
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest requests first
        verbose_name = 'Exchange Request'
        verbose_name_plural = 'Exchange Requests'

    def __str__(self):
        return f"{self.requester.first_name} → {self.receiver.first_name} ({self.skill.name})"
