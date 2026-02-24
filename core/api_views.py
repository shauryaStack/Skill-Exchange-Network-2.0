"""
api_views.py — REST API Endpoints (JSON responses)

These views return JSON instead of HTML — they're used by:
    - AJAX calls from the frontend (JavaScript fetch requests)
    - Mobile apps or any external client

All API endpoints follow this pattern:
    - Accept JSON in request body (for POST)
    - Return JSON with 'status' and 'message' keys
    - Use proper HTTP status codes (200, 400, 403, 404)

Endpoints:
    POST /api/request-exchange/          → Send an exchange request via AJAX
    GET  /api/notifications/             → Get pending request counts
    POST /api/exchanges/<id>/schedule/   → Schedule a session
    GET  /api/live-users/                → Get platform statistics
    GET  /api/health/                    → API health check
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import ExchangeRequest, User, Skill


@login_required
@csrf_exempt       # Exempt from CSRF because this is called via AJAX with JSON body
@require_http_methods(["POST"])
def api_request_exchange(request):
    """
    Handle exchange requests via AJAX (called from match.html).

    This is the API version of the form-based request_exchange view in views.py.
    The frontend sends JSON data instead of form data.

    Expected JSON body:
        {
            "teacher_id": 5,
            "skill_name": "Python Programming",
            "offering_skill": "Web Design",
            "preferred_time": "Weekends",
            "message": "I'd love to learn Python!"
        }
    """
    try:
        data = json.loads(request.body)
        teacher_id = data.get('teacher_id')
        skill_name = data.get('skill_name')
        offering_skill = data.get('offering_skill')
        preferred_time = data.get('preferred_time')
        message = data.get('message', '')

        teacher = User.objects.get(id=teacher_id)
        skill = Skill.objects.get(name=skill_name)

        # Don't allow users to send requests to themselves
        if teacher == request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'You cannot request exchange with yourself!'
            }, status=400)

        # Prevent duplicate pending requests for the same teacher+skill combo
        existing = ExchangeRequest.objects.filter(
            requester=request.user,
            receiver=teacher,
            skill=skill,
            status='pending'
        ).exists()

        if existing:
            return JsonResponse({
                'status': 'error',
                'message': 'You already have a pending request with this teacher!'
            }, status=400)

        # Create the exchange request in the database
        ExchangeRequest.objects.create(
            requester=request.user,
            receiver=teacher,
            skill=skill,
            offering_skill=offering_skill,
            preferred_time=preferred_time,
            message=message
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Request sent successfully!'
        })

    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Teacher not found!'
        }, status=404)
    except Skill.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Skill not found!'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["GET"])
def api_notifications(request):
    """
    Get notification counts for the current logged-in user.
    Used by the navbar to show badge counts (e.g., "3 pending requests").

    Returns:
        pending_requests: Requests waiting for this user's response
        sent_requests: Requests this user has sent that are still pending
        accepted_exchanges: Total active exchanges this user is part of
        total_notifications: Same as pending_requests (used for badge)
    """
    pending_count = ExchangeRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).count()

    sent_count = ExchangeRequest.objects.filter(
        requester=request.user,
        status='pending'
    ).count()

    # Count accepted exchanges where user is either requester or receiver
    accepted_count = ExchangeRequest.objects.filter(
        requester=request.user,
        status='accepted'
    ).count() + ExchangeRequest.objects.filter(
        receiver=request.user,
        status='accepted'
    ).count()

    return JsonResponse({
        'pending_requests': pending_count,
        'sent_requests': sent_count,
        'accepted_exchanges': accepted_count,
        'total_notifications': pending_count
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def api_schedule_session(request, exchange_id):
    """
    Schedule a date and time for an accepted exchange session.

    Only participants (requester or receiver) can schedule the session.
    After saving, sends a notification to the partner.

    Expected JSON body:
        {
            "date": "2026-03-01",
            "time": "14:00"
        }
    """
    try:
        data = json.loads(request.body)
        session_date = data.get('date')
        session_time = data.get('time')

        # Only fetch accepted exchanges — can't schedule pending/rejected ones
        exchange = ExchangeRequest.objects.get(
            id=exchange_id,
            status='accepted'
        )

        # Authorization check — only participants can schedule
        if exchange.requester != request.user and exchange.receiver != request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'You are not authorized to schedule this session!'
            }, status=403)

        # Save the schedule
        exchange.scheduled_date = session_date
        exchange.scheduled_time = session_time
        exchange.save()

        # Send notification to the partner (the other user)
        try:
            from .utils import send_schedule_notification
            send_schedule_notification(exchange, request.user)
        except Exception as e:
            # Don't fail the whole request if notification fails
            print(f"Notification error: {e}")

        return JsonResponse({
            'status': 'success',
            'message': f'Session scheduled for {session_date} at {session_time}. Notification sent!',
            'exchange_id': exchange_id,
            'date': session_date,
            'time': session_time
        })

    except ExchangeRequest.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Exchange not found or not accepted yet!'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def api_live_users(request):
    """
    Get platform-wide statistics. No login required.
    Used on the home page to show live counters.
    """
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_skills = Skill.objects.count()
    total_exchanges = ExchangeRequest.objects.filter(status='accepted').count()

    return JsonResponse({
        'total_users': total_users,
        'active_users': active_users,
        'total_skills': total_skills,
        'total_exchanges': total_exchanges
    })


@require_http_methods(["GET"])
def api_health(request):
    """
    Health check endpoint — used to verify the API is running.
    Returns the API version and lists all available endpoints.
    """
    return JsonResponse({
        "status": "ok",
        "message": "Skill Exchange API v1.0 working!",
        "version": "1.0.0",
        "endpoints": [
            "/api/health/",
            "/api/notifications/",
            "/api/request-exchange/",
            "/api/live-users/",
            "/api/exchanges/<id>/schedule/"
        ]
    })
