"""
views.py — Main View Functions (Page Rendering & Form Handling)

This is the largest file — it handles all the page views and form submissions.
Each function here either:
    1. Renders an HTML template (GET requests)
    2. Processes form data and redirects (POST requests)

Sections:
    - Authentication Views: login, register, logout, Firebase login
    - Main Views: index (home), profile, browse, match, sessions
    - Exchange Request Views: send, accept, reject requests
    - Skill Management Views: add/remove teaching skills
    - Session Management Views: reschedule, save meeting links, send notifications

Important concepts:
    - @login_required: Redirects to login page if user isn't authenticated
    - @csrf_protect: Prevents Cross-Site Request Forgery attacks on forms
    - messages.success/error: Flash messages shown to user after redirect
    - select_related(): Reduces database queries by joining related tables
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
import json
from .models import Skill, User, UserTeaches, ExchangeRequest
from .utils import send_schedule_notification, send_meeting_link_notification, send_custom_notification


# ==================== AUTHENTICATION VIEWS ====================

@csrf_protect
def login_view(request):
    """
    Handle user login with email and password.

    GET: Show the login form
    POST: Validate credentials and log the user in

    Why we use email instead of username?
    - More user-friendly; people remember their email better
    - We look up the User by email, then check the password
    """
    # Already logged in → go to home page
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please provide both email and password!")
            return render(request, "core/login.html")

        try:
            # Step 1: Find user by email
            user = User.objects.get(email=email)

            # Step 2: Verify password (Django hashes and compares automatically)
            if user.check_password(password):
                # Step 3: Create a session for this user
                # We specify the backend because we have multiple auth backends (Django + Firebase)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")

                # Redirect to the page they were trying to access, or home
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, "Incorrect password!")

        except User.DoesNotExist:
            messages.error(request, "No account found with this email!")
        except Exception as e:
            messages.error(request, f"Login error: {str(e)}")

    return render(request, "core/login.html")


@csrf_exempt
@require_http_methods(["POST"])
def firebase_login(request):
    """
    Handle Firebase authentication — called via AJAX from the frontend.

    This is for Google Sign-In or other Firebase auth methods.
    The frontend authenticates with Firebase, gets user data, and sends it here.
    We then create/find a matching Django user and start a Django session.

    Why both Firebase AND Django auth?
    - Firebase handles the social login UI (Google popup, etc.)
    - Django handles server-side sessions, permissions, and database access
    """
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        email = data.get('email')
        display_name = data.get('displayName', '')
        photo_url = data.get('photoURL', '')

        if not email:
            return JsonResponse({
                'success': False,
                'error': 'Email is required'
            }, status=400)

        # Find existing user or create a new one based on email
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],  # Use email prefix as username
                'first_name': display_name.split(' ')[0] if display_name else '',
                'last_name': ' '.join(display_name.split(' ')[1:]) if display_name else ''
            }
        )

        # New Firebase users can't log in with password — they use Firebase only
        if created:
            user.set_unusable_password()
            user.save()

        # Start a Django session for this user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return JsonResponse({
            'success': True,
            'message': f'Welcome {user.first_name or user.username}!',
            'user': {
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip(),
                'created': created  # Frontend can show "account created" vs "welcome back"
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_protect
def register_view(request):
    """
    Handle new user registration.

    GET: Show the registration form with available skills
    POST: Create user account, assign teaching skills, auto-login

    This view also seeds the database with 35 default skills on first run
    (when no skills exist yet). This ensures the registration form always
    has skills to choose from.
    """
    # Already logged in → go to home page
    if request.user.is_authenticated:
        return redirect('index')

    # Seed default skills if the database is empty (first-time setup)
    if not Skill.objects.exists():
        Skill.objects.bulk_create([
            # Programming & Development
            Skill(name="Python Programming", category="Programming"),
            Skill(name="JavaScript", category="Programming"),
            Skill(name="Java Programming", category="Programming"),
            Skill(name="C++ Programming", category="Programming"),
            Skill(name="React.js", category="Web Development"),
            Skill(name="Node.js", category="Web Development"),
            Skill(name="Django", category="Web Development"),
            Skill(name="Flask", category="Web Development"),
            Skill(name="Angular", category="Web Development"),
            Skill(name="Vue.js", category="Web Development"),

            # Mobile Development
            Skill(name="Android Development", category="Mobile Development"),
            Skill(name="iOS Development", category="Mobile Development"),
            Skill(name="React Native", category="Mobile Development"),
            Skill(name="Flutter", category="Mobile Development"),

            # Data & AI
            Skill(name="Data Science", category="Data & AI"),
            Skill(name="Machine Learning", category="Data & AI"),
            Skill(name="Deep Learning", category="Data & AI"),
            Skill(name="Data Analysis", category="Data & AI"),
            Skill(name="SQL & Databases", category="Data & AI"),

            # Design
            Skill(name="UI/UX Design", category="Design"),
            Skill(name="Graphic Design", category="Design"),
            Skill(name="Adobe Photoshop", category="Design"),
            Skill(name="Figma", category="Design"),
            Skill(name="Video Editing", category="Design"),
            Skill(name="3D Modeling", category="Design"),

            # Business & Marketing
            Skill(name="Digital Marketing", category="Marketing"),
            Skill(name="Content Writing", category="Marketing"),
            Skill(name="SEO", category="Marketing"),
            Skill(name="Social Media Marketing", category="Marketing"),

            # Other Skills
            Skill(name="Cloud Computing", category="Technology"),
            Skill(name="Cybersecurity", category="Technology"),
            Skill(name="DevOps", category="Technology"),
            Skill(name="Blockchain", category="Technology"),
            Skill(name="Game Development", category="Technology"),
        ])

    if request.method == 'POST':
        # --- Collect form data ---
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        name = request.POST.get('name', '').strip()

        # Support both separate first/last fields and a combined "name" field
        if name and not first_name:
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        email = request.POST.get('email', '').strip().lower()
        division = request.POST.get('division', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        password2 = request.POST.get('password2', '')  # Alternative field name from some forms

        # Use whichever confirm password field has a value
        if not confirm_password:
            confirm_password = password2

        teach_skills = request.POST.getlist('teach_skills')  # List of selected skill IDs
        available_time = request.POST.get('available_time', 'Flexible')

        # --- Validation ---
        if not all([first_name, email, password]):
            messages.error(request, "Please fill all required fields!")
            return render(request, "core/register.html", {"skills": Skill.objects.all()})

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters!")
            return render(request, "core/register.html", {"skills": Skill.objects.all()})

        if confirm_password and password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return render(request, "core/register.html", {"skills": Skill.objects.all()})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "core/register.html", {"skills": Skill.objects.all()})

        # Generate a unique username from the email prefix
        # e.g., "john@gmail.com" → "john", or "john1" if "john" is taken
        username = email.split('@')[0]
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        try:
            # --- Create the user account ---
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password  # Django automatically hashes this
            )

            # Set custom fields that aren't in create_user()
            user.division = division
            user.phone = phone
            user.save()

            # --- Assign teaching skills ---
            # Create UserTeaches entries for each skill the user selected
            if teach_skills:
                for skill_id in teach_skills:
                    try:
                        skill = Skill.objects.get(id=int(skill_id))
                        UserTeaches.objects.create(
                            user=user,
                            skill=skill,
                            available_time=available_time
                        )
                    except (Skill.DoesNotExist, ValueError):
                        # Skip invalid skill IDs silently
                        continue

            # Auto-login after registration so user doesn't have to log in again
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome {first_name}! Your account has been created!")
            return redirect('index')

        except Exception as e:
            messages.error(request, f"Registration error: {str(e)}")
            return render(request, "core/register.html", {"skills": Skill.objects.all()})

    # GET request — show the registration form with all available skills
    return render(request, "core/register.html", {"skills": Skill.objects.all()})


def logout_view(request):
    """Handle user logout — clears the session and redirects to home."""
    if request.user.is_authenticated:
        user_name = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f"Goodbye {user_name}! Logged out successfully!")
    return redirect('index')


# ==================== MAIN VIEWS ====================

def index(request):
    """
    Home page — shows platform statistics and, for logged-in users,
    their personal stats (how many skills they teach, pending requests, etc.)
    """
    total_users = User.objects.count()
    total_skills = Skill.objects.count()
    total_exchanges = ExchangeRequest.objects.filter(status='accepted').count()

    context = {
        'total_users': total_users,
        'total_skills': total_skills,
        'total_exchanges': total_exchanges,
    }

    if request.user.is_authenticated:
        # Add personal stats for logged-in users
        teaches_count = UserTeaches.objects.filter(user=request.user).count()
        incoming_count = ExchangeRequest.objects.filter(
            receiver=request.user,
            status='pending'
        ).count()
        context.update({
            'teaches_count': teaches_count,
            'incoming_count': incoming_count,
        })

    return render(request, "core/index.html", context)


@login_required
def profile_view(request):
    """
    User profile/dashboard — shows everything related to the current user:
        - Skills they teach
        - Incoming exchange requests (pending approval)
        - Requests they've sent
        - Active (accepted) exchanges

    select_related() is used to avoid the "N+1 query problem":
    Without it, accessing request.requester.first_name would trigger
    a separate DB query for each request. select_related joins the tables
    in a single query.
    """
    teaches = UserTeaches.objects.filter(user=request.user).select_related('skill')

    incoming_requests = ExchangeRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('requester', 'skill').order_by('-created_at')

    sent_requests = ExchangeRequest.objects.filter(
        requester=request.user
    ).select_related('receiver', 'skill').order_by('-created_at')

    # Q objects allow OR conditions: where user is requester OR receiver
    accepted_exchanges = ExchangeRequest.objects.filter(
        Q(requester=request.user) | Q(receiver=request.user),
        status='accepted'
    ).select_related('requester', 'receiver', 'skill')

    return render(request, "core/profile.html", {
        'teaches': teaches,
        'incoming_requests': incoming_requests,
        'sent_requests': sent_requests,
        'accepted_exchanges': accepted_exchanges,
    })


def browse_view(request):
    """
    Browse all available skills with search and category filtering.

    annotate(teacher_count=Count('userteaches')) adds a virtual field
    to each skill showing how many teachers are available for it.
    This is calculated in the database, not in Python, so it's fast.
    """
    # Add teacher_count to each skill via annotation
    skills = Skill.objects.annotate(teacher_count=Count('userteaches'))

    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '').strip()

    # Filter by search query (matches skill name OR category)
    if search_query:
        skills = skills.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Filter by exact category
    if selected_category:
        skills = skills.filter(category=selected_category)

    # Get unique categories for the filter dropdown
    categories = Skill.objects.values_list('category', flat=True).distinct().order_by('category')

    return render(request, "core/browse.html", {
        "skills": skills.order_by('name'),
        "search_query": search_query,
        "selected_category": selected_category,
        "categories": categories,
        "total_skills": skills.count(),
    })


def match_view(request):
    """
    Find teachers for a specific skill.
    Accessed via: /match/?skill_id=5

    Shows all users who have registered to teach the given skill,
    along with their proficiency level and availability.
    """
    skill_id = request.GET.get('skill_id')
    teachers = []
    skill = None

    if skill_id:
        try:
            skill = Skill.objects.get(id=skill_id)
            # Get all UserTeaches entries for this skill, with related user data
            teachers = UserTeaches.objects.filter(
                skill=skill
            ).select_related('user', 'skill')
        except Skill.DoesNotExist:
            messages.error(request, "Skill not found!")
        except Exception as e:
            messages.error(request, f"Error loading teachers: {str(e)}")

    return render(request, "core/match.html", {
        "teachers": teachers,
        "skill": skill,
    })


@login_required
def sessions_view(request):
    """
    View user's learning sessions (only accepted exchanges).

    Splits sessions into two views:
        - Teaching: Sessions where this user is the receiver (someone wants to learn from them)
        - Learning: Sessions where this user is the requester (they want to learn from someone)
    """
    teaching_sessions = ExchangeRequest.objects.filter(
        receiver=request.user,
        status='accepted'
    ).select_related('requester', 'skill')

    learning_sessions = ExchangeRequest.objects.filter(
        requester=request.user,
        status='accepted'
    ).select_related('receiver', 'skill')

    return render(request, "core/sessions.html", {
        'teaching_sessions': teaching_sessions,
        'learning_sessions': learning_sessions,
    })


# ==================== EXCHANGE REQUEST VIEWS ====================

@csrf_protect
@login_required
def request_exchange(request):
    """
    Send an exchange request to a teacher (form-based version).

    This is the traditional HTML form version. The API version is in api_views.py.
    After creating the request, redirects to the profile page to see it.
    """
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        skill_id = request.POST.get('skill_id')
        skill_name = request.POST.get('skill_name')
        offering_skill = request.POST.get('offering_skill', '').strip()
        preferred_time = request.POST.get('preferred_time', 'Flexible')
        message = request.POST.get('message', '').strip()

        if not all([teacher_id, offering_skill]):
            messages.error(request, "Missing required information!")
            return redirect('browse')

        try:
            teacher = User.objects.get(id=teacher_id)

            # Skill can be identified by ID or name (different forms send different data)
            if skill_id:
                skill = Skill.objects.get(id=skill_id)
            elif skill_name:
                skill = Skill.objects.get(name=skill_name)
            else:
                messages.error(request, "Skill not specified!")
                return redirect('browse')

            # Can't exchange with yourself
            if teacher == request.user:
                messages.error(request, "You cannot request exchange with yourself!")
                return redirect('browse')

            # Check for duplicate pending requests
            existing = ExchangeRequest.objects.filter(
                requester=request.user,
                receiver=teacher,
                skill=skill,
                status='pending'
            ).exists()

            if existing:
                messages.warning(request, "You already have a pending request with this teacher!")
                return redirect('profile')

            # Create the exchange request
            ExchangeRequest.objects.create(
                requester=request.user,
                receiver=teacher,
                skill=skill,
                offering_skill=offering_skill,
                preferred_time=preferred_time,
                message=message
            )

            messages.success(request, f"Request sent to {teacher.first_name}!")
            return redirect('profile')

        except User.DoesNotExist:
            messages.error(request, "Teacher not found!")
        except Skill.DoesNotExist:
            messages.error(request, "Skill not found!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('browse')


@csrf_protect
@login_required
def accept_exchange(request, exchange_id):
    """
    Accept an incoming exchange request.

    Only the receiver can accept their own requests.
    The query filters by receiver=request.user to enforce this.
    """
    if request.method == 'POST':
        try:
            exchange = ExchangeRequest.objects.get(
                id=exchange_id,
                receiver=request.user,   # Only the receiver can accept
                status='pending'          # Can only accept pending requests
            )

            exchange.status = 'accepted'
            exchange.save()

            messages.success(request, f"Exchange with {exchange.requester.first_name} accepted!")

        except ExchangeRequest.DoesNotExist:
            messages.error(request, "Request not found or already processed!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('profile')


@csrf_protect
@login_required
def reject_exchange(request, exchange_id):
    """
    Reject an incoming exchange request.
    Same authorization logic as accept_exchange — only the receiver can reject.
    """
    if request.method == 'POST':
        try:
            exchange = ExchangeRequest.objects.get(
                id=exchange_id,
                receiver=request.user,
                status='pending'
            )

            exchange.status = 'rejected'
            exchange.save()

            messages.info(request, "Request declined!")

        except ExchangeRequest.DoesNotExist:
            messages.error(request, "Request not found!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('profile')


# ==================== SKILL MANAGEMENT VIEWS ====================

@login_required
def add_skill(request):
    """
    Add a skill to the user's teaching list.

    GET: Show form with all available skills (graying out ones already taught)
    POST: Create a new UserTeaches entry linking the user to the skill
    """
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        proficiency = request.POST.get('proficiency', 'intermediate')
        available_time = request.POST.get('available_time', 'Flexible')
        notes = request.POST.get('notes', '').strip()

        if not skill_id:
            messages.error(request, "Please select a skill!")
            return redirect('add_skill')

        try:
            skill = Skill.objects.get(id=skill_id)

            # Prevent adding the same skill twice
            if UserTeaches.objects.filter(user=request.user, skill=skill).exists():
                messages.warning(request, f"You are already teaching {skill.name}!")
                return redirect('profile')

            # Create the teaching entry
            UserTeaches.objects.create(
                user=request.user,
                skill=skill,
                proficiency=proficiency,
                available_time=available_time,
                notes=notes
            )

            messages.success(request, f"Great! You can now teach {skill.name}!")
            return redirect('profile')

        except Skill.DoesNotExist:
            messages.error(request, "Skill not found!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    # GET request — prepare the form
    skills = Skill.objects.all().order_by('category', 'name')

    # Get IDs of skills user already teaches (to gray them out in the form)
    teaching_skill_ids = UserTeaches.objects.filter(
        user=request.user
    ).values_list('skill_id', flat=True)

    context = {
        'skills': skills,
        'teaching_skill_ids': list(teaching_skill_ids),
    }
    return render(request, 'core/add_skill.html', context)


@login_required
@csrf_protect
def remove_skill(request, teach_id):
    """
    Remove a skill from the user's teaching list.
    The teach_id is the UserTeaches entry ID, not the Skill ID.
    Filtering by user=request.user ensures users can only remove their own skills.
    """
    if request.method == 'POST':
        try:
            teach = UserTeaches.objects.get(id=teach_id, user=request.user)
            skill_name = teach.skill.name
            teach.delete()
            messages.success(request, f"Removed {skill_name} from your teaching list!")
        except UserTeaches.DoesNotExist:
            messages.error(request, "Skill entry not found!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('profile')


# ==================== SESSION MANAGEMENT VIEWS ====================

@csrf_protect
@login_required
def reschedule_session(request):
    """
    Reschedule an accepted session to a new date/time.

    Only participants (requester or receiver) can reschedule.
    After saving, sends a notification to the partner.
    """
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        new_date = request.POST.get('new_date')
        new_time = request.POST.get('new_time')

        try:
            session = ExchangeRequest.objects.get(
                id=session_id,
                status='accepted'
            )

            # Authorization: only participants can reschedule
            if session.requester == request.user or session.receiver == request.user:
                session.scheduled_date = new_date
                session.scheduled_time = new_time
                session.save()

                # Notify the partner about the schedule change
                try:
                    send_schedule_notification(session, request.user)
                except Exception as e:
                    print(f"Notification error: {e}")

                messages.success(request, f"Session rescheduled to {new_date} at {new_time}! Notification sent.")
            else:
                messages.error(request, "You're not authorized to reschedule this session!")

        except ExchangeRequest.DoesNotExist:
            messages.error(request, "Session not found!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('sessions')


@csrf_protect
@login_required
def save_meeting_link(request):
    """
    Save a meeting link (Google Meet / Teams URL) for a session.
    Called via AJAX — returns JSON instead of redirecting.

    Normalizes platform names so different input formats
    (e.g., "Google Meet", "google_meet", "googlemeet") all map to the same value.
    """
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        meeting_link = request.POST.get('meeting_link')
        platform = request.POST.get('platform', '').lower().replace(' ', '_')

        # Normalize platform names to match PLATFORM_CHOICES in the model
        platform_map = {
            'google_meet': 'google_meet',
            'googlemeet': 'google_meet',
            'google meet': 'google_meet',
            'teams': 'teams',
            'microsoft_teams': 'teams',
            'microsoft teams': 'teams',
        }
        platform = platform_map.get(platform, platform)

        try:
            session = ExchangeRequest.objects.get(
                id=session_id,
                status='accepted'
            )

            # Authorization check
            if session.requester == request.user or session.receiver == request.user:
                session.meeting_link = meeting_link
                session.meeting_platform = platform
                session.save()

                # Notify partner about the new meeting link
                try:
                    send_meeting_link_notification(session, request.user)
                except Exception as e:
                    print(f"Notification error: {e}")

                return JsonResponse({'success': True, 'message': 'Link saved and notification sent!'})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

        except ExchangeRequest.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_protect
@login_required
def send_notification(request):
    """
    Send an email or WhatsApp notification to the session partner.
    Called via AJAX from the sessions page.

    The user clicks "Send Email" or "Send WhatsApp" button,
    and this view composes and sends the appropriate message.

    notify_type: 'email' or 'whatsapp'
    """
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        notify_type = request.POST.get('notify_type', 'email')

        try:
            session = ExchangeRequest.objects.get(
                id=session_id,
                status='accepted'
            )

            # Authorization check
            if session.requester != request.user and session.receiver != request.user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            # Find the partner (the other person in the exchange)
            if session.requester == request.user:
                partner = session.receiver
            else:
                partner = session.requester

            # Format session details for the notification
            platform_display = session.get_meeting_platform_display() if session.meeting_platform else "Online"
            date_str = session.scheduled_date.strftime("%B %d, %Y") if session.scheduled_date else "To be confirmed"
            time_str = session.scheduled_time.strftime("%I:%M %p") if session.scheduled_time else "To be confirmed"

            # Build email body
            subject = f"🔗 Skill Exchange Session: {session.skill.name}"
            body = (
                f"Hi {partner.first_name or partner.username},\n\n"
                f"Here are the details for your skill exchange session:\n\n"
                f"📚 Skill: {session.skill.name}\n"
                f"📅 Date: {date_str}\n"
                f"⏰ Time: {time_str}\n"
                f"🖥️ Platform: {platform_display}\n"
            )
            if session.meeting_link:
                body += f"🔗 Meeting Link: {session.meeting_link}\n"
            body += (
                f"\nSent by: {request.user.first_name or request.user.username}\n\n"
                f"— Skill Exchange Network"
            )

            # Build WhatsApp body (shorter format for mobile)
            whatsapp_body = (
                f"📅 *Skill Exchange Session*\n\n"
                f"📚 Skill: {session.skill.name}\n"
                f"📅 Date: {date_str}\n"
                f"⏰ Time: {time_str}\n"
                f"🖥️ Platform: {platform_display}\n"
            )
            if session.meeting_link:
                whatsapp_body += f"🔗 Link: {session.meeting_link}\n"

            # Send the appropriate notification type
            if notify_type == 'email':
                from .utils import send_email_to_user
                send_email_to_user(partner.email, subject, body)
                return JsonResponse({'success': True, 'message': f'Email sent to {partner.email}!'})

            elif notify_type == 'whatsapp':
                from .utils import send_whatsapp_to_user
                if not partner.phone:
                    return JsonResponse({'error': 'Partner has no phone number on their profile'}, status=400)
                send_whatsapp_to_user(partner.phone, whatsapp_body)
                return JsonResponse({'success': True, 'message': f'WhatsApp sent to {partner.phone}!'})

            else:
                return JsonResponse({'error': 'Invalid notify_type'}, status=400)

        except ExchangeRequest.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
