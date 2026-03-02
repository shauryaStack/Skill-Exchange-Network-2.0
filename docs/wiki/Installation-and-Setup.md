# Installation & Setup

This guide walks you through every step required to run **Skill Exchange Network 2.0** on your local machine.

---

## Prerequisites

| Requirement | Minimum Version |
| :--- | :--- |
| Python | 3.10+ |
| pip | 22+ |
| Git | Any recent version |

> **Optional**: A [Firebase](https://console.firebase.google.com) project (for Google Sign-In) and a [Twilio](https://www.twilio.com) account (for WhatsApp notifications).

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/shauryapradhan546/Skill-Exchange-Network-2.0.git
cd Skill-Exchange-Network-2.0
```

---

## Step 2 — Create and Activate a Virtual Environment

Using a virtual environment keeps dependencies isolated from your global Python installation.

```bash
# Create the environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt once it is active.

---

## Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

Key packages installed:

| Package | Purpose |
| :--- | :--- |
| `Django>=4.2` | Web framework |
| `djangorestframework>=3.14` | REST API support |
| `firebase-admin>=6.4` | Firebase / Google Sign-In |
| `twilio>=8.0` | WhatsApp notifications |
| `python-dotenv>=1.0` | Load `.env` variables |

---

## Step 4 — Configure Environment Variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Open `.env` in a text editor and set the following values:

```dotenv
# Django
SECRET_KEY=your-random-secret-key   # e.g. generated with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=True                           # Set to False in production

# Firebase (Google Sign-In)
FIREBASE_API_KEY=...
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=...
FIREBASE_APP_ID=...
FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX

# Twilio — WhatsApp notifications (optional)
# TWILIO_ACCOUNT_SID=...
# TWILIO_AUTH_TOKEN=...
# TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

See [Configuration](Configuration.md) for detailed explanations of every variable.

---

## Step 5 — Apply Database Migrations

Django creates all database tables from the model definitions:

```bash
python manage.py makemigrations
python manage.py migrate
```

The project uses **SQLite** by default (`db.sqlite3`). No additional database server is needed for local development.

---

## Step 6 — (Optional) Create a Superuser

A superuser lets you access the Django admin panel at `/admin/`.

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---

## Step 7 — Run the Development Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. The application is ready!

| URL | Description |
| :--- | :--- |
| http://127.0.0.1:8000/ | Homepage |
| http://127.0.0.1:8000/register/ | Create a new account |
| http://127.0.0.1:8000/admin/ | Django admin panel |
| http://127.0.0.1:8000/api/health/ | API health check (JSON) |

---

## Resetting the Database

If you need to start fresh, follow the instructions in `Steps to Reset the Database.txt` in the project root, or run:

```bash
# Delete the SQLite database file
rm db.sqlite3

# Re-run migrations
python manage.py migrate
```

---

## Common Issues

| Problem | Solution |
| :--- | :--- |
| `ModuleNotFoundError` | Make sure your virtual environment is activated and `pip install -r requirements.txt` has been run |
| `django.core.exceptions.ImproperlyConfigured` about `SECRET_KEY` | Ensure `.env` exists and `SECRET_KEY` is set |
| Firebase errors on startup | Set `FIREBASE_PROJECT_ID` correctly in `.env`; Firebase integration is optional for local dev |
| Port already in use | Run on a different port: `python manage.py runserver 8080` |
