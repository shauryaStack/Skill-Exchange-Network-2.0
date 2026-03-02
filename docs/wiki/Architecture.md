# Architecture

This page explains the internal structure of Skill Exchange Network 2.0 — how the code is organized, what every file does, and how all the pieces fit together.

---

## High-Level Architecture

The project follows Django's **MTV (Model – Template – View)** pattern, a variant of MVC:

```
Browser  ──►  urls.py  ──►  views.py  ──►  models.py  (Database)
                                 │
                                 ▼
                           templates/  (HTML)
                                 │
                                 ▼
                            Browser  (rendered page)
```

| Django Layer | Role | Analogy |
| :--- | :--- | :--- |
| **Model** (`models.py`) | Defines database tables and relationships | Storage room & ingredients |
| **Template** (`templates/`) | HTML pages rendered and sent to the browser | The plate served to the guest |
| **View** (`views.py`) | Processes requests, fetches data, passes it to templates | The chef |
| **URL Router** (`urls.py`) | Maps incoming URLs to the right view function | The waiter taking orders |
| **Utils** (`utils.py`) | Handles email and WhatsApp notifications | A delivery driver |

---

## Project Directory Structure

```
Skill-Exchange-Network-2.0/
├── core/                          # Main Django application
│   ├── models.py                  # Database models (User, Skill, ExchangeRequest)
│   ├── views.py                   # Page views and form handlers
│   ├── api_views.py               # REST API endpoints (JSON responses)
│   ├── urls.py                    # URL routing for the core app
│   ├── utils.py                   # Email & WhatsApp notification helpers
│   ├── authentication.py          # Firebase authentication backend
│   ├── context_processors.py      # Template context helpers
│   ├── admin.py                   # Django admin panel registration
│   ├── apps.py                    # App configuration
│   ├── tests.py                   # Unit tests
│   ├── migrations/                # Database migration files
│   ├── static/                    # CSS, JavaScript, images
│   └── templates/core/            # HTML templates
│       ├── base.html              # Base layout (navbar, footer)
│       ├── index.html             # Homepage
│       ├── login.html             # Login form
│       ├── register.html          # Registration form
│       ├── profile.html           # User dashboard
│       ├── browse.html            # Browse skills
│       ├── match.html             # Teacher listings for a skill
│       └── sessions.html          # Active sessions view
│
├── updated_skill_exchange_network/ # Django project settings package
│   ├── settings.py                # Global Django settings
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI server entry point
│   └── asgi.py                    # ASGI server entry point
│
├── manage.py                      # Django management CLI
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── db.sqlite3                     # SQLite database (development only)
├── docs/wiki/                     # Project wiki documentation
└── README.md                      # Repository overview
```

---

## Data Models

### `User` (extends `AbstractUser`)

Inherits all of Django's built-in authentication fields and adds:

| Field | Type | Description |
| :--- | :--- | :--- |
| `division` | `CharField(100)` | The user's department (e.g., "Computer Science") |
| `phone` | `CharField(15)` | Phone number for WhatsApp notifications |
| `firebase_uid` | `CharField(255)` | Links the Django account to a Firebase/Google account |

### `Skill`

A catalogue of skills that can be taught or learned on the platform.

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | `CharField(100)` | Unique skill name (e.g., "Python Programming") |
| `category` | `CharField(50)` | Grouping (e.g., "Programming", "Design") |
| `created_at` | `DateTimeField` | Auto-set on creation |

### `UserTeaches` (through model)

Connects a `User` to a `Skill` they can teach. Acts as a many-to-many through table so extra fields can be stored on the relationship.

| Field | Type | Description |
| :--- | :--- | :--- |
| `user` | FK → `User` | The teacher |
| `skill` | FK → `Skill` | The skill being taught |
| `proficiency` | `CharField` | `beginner` / `intermediate` / `advanced` / `expert` |
| `available_time` | `CharField(100)` | When the teacher is free (e.g., "Weekends") |
| `notes` | `TextField(500)` | Optional teaching-style notes |

Unique constraint: `(user, skill)` — a user can only list each skill once.

### `ExchangeRequest`

Represents a skill-exchange request between two users.

| Field | Type | Description |
| :--- | :--- | :--- |
| `requester` | FK → `User` | User who sent the request |
| `receiver` | FK → `User` | User who received the request (the teacher) |
| `skill` | FK → `Skill` | The skill being requested |
| `offering_skill` | `CharField(100)` | What the requester offers to teach in return |
| `preferred_time` | `CharField(50)` | When the requester prefers to meet |
| `message` | `TextField` | Optional personal message |
| `status` | `CharField` | `pending` → `accepted` / `rejected` → `completed` |
| `meeting_link` | `URLField` | Google Meet or Teams link |
| `meeting_platform` | `CharField` | `google_meet` or `teams` |
| `scheduled_date` | `DateField` | Date of the session |
| `scheduled_time` | `TimeField` | Time of the session |
| `created_at` | `DateTimeField` | Auto-set on creation |
| `updated_at` | `DateTimeField` | Auto-updated on every save |

#### Status Lifecycle

```
pending  ──►  accepted  ──►  completed
         └──►  rejected
```

---

## Authentication Flow

The application supports two authentication methods:

### 1. Email / Password (Django Auth)
1. User submits email + password on `/login/`
2. `login_view` finds the `User` by email, verifies the password hash
3. Django creates a session cookie

### 2. Google Sign-In (Firebase)
1. User clicks "Sign in with Google" on the login page
2. Firebase SDK authenticates the user client-side and returns an ID token
3. The token is posted to `/firebase-login/`
4. `firebase_login` view verifies the token with `firebase-admin`, then creates or retrieves the Django `User` record using `firebase_uid`
5. Django creates a session

---

## Notification System

Notifications are handled by helper functions in `core/utils.py`:

| Function | Trigger | Channel |
| :--- | :--- | :--- |
| `send_session_email` | Any session event | Email (Gmail SMTP) |
| `send_whatsapp_to_user` | Any session event | WhatsApp (Twilio) |
| `send_schedule_notification` | Session date/time is set or changed | Email + WhatsApp |
| `send_meeting_link_notification` | A meeting link is added | Email + WhatsApp |

Both channels are attempted for every notification. A failure in one channel (e.g., Twilio is not configured) does not block the other.

---

## Request / Response Cycle Example

**Emma requests a Python lesson from John:**

```
1. Emma visits /browse/
   └─► browse_view() queries Skill.objects.all(), renders browse.html

2. Emma clicks "Python" → /match/?skill_id=5
   └─► match_view() queries UserTeaches for skill_id=5, renders match.html

3. Emma clicks "Request" → POST /api/request-exchange/ (AJAX)
   └─► api_request_exchange() creates ExchangeRequest(status='pending')

4. John opens /profile/
   └─► profile_view() fetches received_requests for John, renders profile.html

5. John clicks "Accept" → POST /accept-exchange/42/
   └─► accept_exchange() sets status='accepted', calls send_schedule_notification()

6. Email and WhatsApp alerts are sent to Emma
```
