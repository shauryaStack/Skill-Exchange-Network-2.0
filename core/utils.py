"""
utils.py — Notification Helpers (Email & WhatsApp)

This file contains all the functions for sending notifications to users.
It handles two channels:
    1. Email — via Django's built-in send_mail (configured in settings.py)
    2. WhatsApp — via Twilio API (optional, requires Twilio credentials)

Architecture:
    - Low-level functions: send_session_email(), send_email_to_user(), send_whatsapp_to_user()
    - High-level functions: send_schedule_notification(), send_meeting_link_notification()
      These compose the message body and call the low-level functions.

The high-level functions figure out WHO to notify (always the partner, not the
person who triggered the action) and WHAT to include in the message.
"""

from django.core.mail import send_mail
from django.conf import settings

# Try to import Twilio — it's optional, the app works without it
try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    # If Twilio isn't installed, set to None so we can check later
    TwilioClient = None


# ============================================
# EMAIL NOTIFICATIONS
# ============================================

def send_session_email(exchange, subject, body_lines):
    """
    Send an email notification about a session to BOTH users.
    Used when both the requester and receiver need to be informed.

    Args:
        exchange: The ExchangeRequest object
        subject: Email subject line
        body_lines: List of strings, each becomes a line in the email body
    """
    # Collect emails, filtering out any empty/None values
    recipients = list(filter(None, [exchange.requester.email, exchange.receiver.email]))
    if not recipients:
        return

    body = "\n".join(body_lines)
    try:
        # fail_silently=True prevents crashes if email sending fails
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
        print(f"✅ Email sent to: {', '.join(recipients)}")
    except Exception as e:
        print(f"❌ Email error: {e}")


def send_email_to_user(email, subject, body):
    """
    Send an email to a single user.
    This is the basic building block — other functions call this.
    """
    if not email:
        return
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)
        print(f"✅ Email sent to: {email}")
    except Exception as e:
        print(f"❌ Email error: {e}")


# ============================================
# WHATSAPP NOTIFICATIONS (via Twilio)
# ============================================

def send_whatsapp_to_user(phone, message_body):
    """
    Send a WhatsApp message to a single user via Twilio.

    Requirements:
        - Twilio Python package must be installed (pip install twilio)
        - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN must be set in settings.py / env vars
        - The recipient's phone number must be registered in your Twilio sandbox

    Note: Phone numbers without a country code default to +91 (India).
    """
    # Skip if no phone number or Twilio isn't installed
    if not phone or not TwilioClient:
        return

    # Skip if Twilio credentials aren't configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("⚠️ Twilio credentials not configured, skipping WhatsApp")
        return

    try:
        client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # type: ignore

        # Ensure phone number has a country code prefix
        clean_phone = phone.strip()
        if not clean_phone.startswith("+"):
            clean_phone = f"+91{clean_phone}"  # Default to India country code

        # Twilio expects "whatsapp:+1234567890" format for WhatsApp messages
        client.messages.create(
            body=message_body,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{clean_phone}",
        )
        print(f"✅ WhatsApp sent to: {clean_phone}")
    except Exception as e:
        print(f"❌ WhatsApp error: {e}")


# ============================================
# HIGH-LEVEL NOTIFICATION FUNCTIONS
# ============================================

def send_schedule_notification(exchange, triggered_by_user):
    """
    Send notification when a session is scheduled or rescheduled.

    Key logic: Notifies the OTHER user (partner), not the one who triggered the action.
    If the requester schedules it → notify the receiver, and vice versa.

    Sends both email and WhatsApp (if configured).
    """
    # Determine who should receive the notification (the partner)
    if exchange.requester == triggered_by_user:
        partner = exchange.receiver
    else:
        partner = exchange.requester

    # Format dates for display — handle cases where date/time aren't set yet
    date_str = exchange.scheduled_date.strftime("%B %d, %Y") if exchange.scheduled_date else "Not set"
    time_str = exchange.scheduled_time.strftime("%I:%M %p") if exchange.scheduled_time else "Not set"
    platform_display = exchange.get_meeting_platform_display() if exchange.meeting_platform else "Not set"

    # --- Build email content ---
    subject = f"📅 Session Scheduled: {exchange.skill.name}"
    body_lines = [
        f"Hi {partner.first_name or partner.username},",
        "",
        f"Your skill exchange session has been scheduled!",
        "",
        f"📚 Skill: {exchange.skill.name}",
        f"📅 Date: {date_str}",
        f"⏰ Time: {time_str}",
        f"🖥️ Platform: {platform_display}",
    ]

    if exchange.meeting_link:
        body_lines.append(f"🔗 Meeting Link: {exchange.meeting_link}")

    body_lines += [
        "",
        f"Scheduled by: {triggered_by_user.first_name or triggered_by_user.username}",
        "",
        "Looking forward to the session!",
        "— Skill Exchange Network",
    ]

    # Send email to partner
    send_email_to_user(partner.email, subject, "\n".join(body_lines))

    # --- Build WhatsApp content (shorter, formatted for mobile) ---
    whatsapp_msg = (
        f"📅 *Session Scheduled!*\n\n"
        f"📚 Skill: {exchange.skill.name}\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time: {time_str}\n"
        f"🖥️ Platform: {platform_display}\n"
    )
    if exchange.meeting_link:
        whatsapp_msg += f"🔗 Link: {exchange.meeting_link}\n"
    whatsapp_msg += f"\nScheduled by {triggered_by_user.first_name or triggered_by_user.username}"

    # Send WhatsApp to partner (only if they have a phone number)
    send_whatsapp_to_user(partner.phone, whatsapp_msg)


def send_meeting_link_notification(exchange, triggered_by_user):
    """
    Send notification when a meeting link is created or updated.
    Same partner-detection logic as send_schedule_notification().
    """
    # Determine partner
    if exchange.requester == triggered_by_user:
        partner = exchange.receiver
    else:
        partner = exchange.requester

    platform_display = exchange.get_meeting_platform_display() if exchange.meeting_platform else "Online"
    date_str = exchange.scheduled_date.strftime("%B %d, %Y") if exchange.scheduled_date else "To be confirmed"
    time_str = exchange.scheduled_time.strftime("%I:%M %p") if exchange.scheduled_time else "To be confirmed"

    # --- Email ---
    subject = f"🔗 Meeting Link Ready: {exchange.skill.name}"
    body = (
        f"Hi {partner.first_name or partner.username},\n\n"
        f"A meeting link has been created for your skill exchange session!\n\n"
        f"📚 Skill: {exchange.skill.name}\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time: {time_str}\n"
        f"🖥️ Platform: {platform_display}\n"
        f"🔗 Meeting Link: {exchange.meeting_link}\n\n"
        f"Click the link above to join when it's time!\n\n"
        f"Created by: {triggered_by_user.first_name or triggered_by_user.username}\n\n"
        f"— Skill Exchange Network"
    )
    send_email_to_user(partner.email, subject, body)

    # --- WhatsApp ---
    whatsapp_msg = (
        f"🔗 *Meeting Link Ready!*\n\n"
        f"📚 Skill: {exchange.skill.name}\n"
        f"🖥️ Platform: {platform_display}\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time: {time_str}\n"
        f"🔗 Join: {exchange.meeting_link}\n\n"
        f"Created by {triggered_by_user.first_name or triggered_by_user.username}"
    )
    send_whatsapp_to_user(partner.phone, whatsapp_msg)


def send_custom_notification(partner_email, partner_phone, subject, body, whatsapp_body=None):
    """
    Generic notification sender — used when you need to send a custom message
    that doesn't fit the schedule/meeting-link templates above.

    Sends email always, WhatsApp only if whatsapp_body is provided.
    """
    send_email_to_user(partner_email, subject, body)
    if whatsapp_body:
        send_whatsapp_to_user(partner_phone, whatsapp_body)
