# Configuration

This page documents every environment variable used by Skill Exchange Network 2.0 and explains how to configure each third-party integration.

---

## Environment File

All configuration is loaded from a `.env` file in the project root. Copy the template before editing:

```bash
cp .env.example .env
```

The file is read at startup by `python-dotenv` via Django's `settings.py`.

> **Never commit your `.env` file to version control.** It contains secrets. It is already listed in `.gitignore`.

---

## Django Core Settings

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `SECRET_KEY` | ✅ Yes | — | Django's cryptographic secret. Generate one with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | No | `True` | Set to `False` in production to disable the debug toolbar and detailed error pages |

### Generating a Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as the value of `SECRET_KEY` in your `.env`.

---

## Firebase Configuration (Google Sign-In)

Firebase enables users to sign in with their Google account. These values come from the Firebase console.

| Variable | Description |
| :--- | :--- |
| `FIREBASE_API_KEY` | Web API key from Firebase project settings |
| `FIREBASE_AUTH_DOMAIN` | `<project-id>.firebaseapp.com` |
| `FIREBASE_PROJECT_ID` | Your Firebase project ID |
| `FIREBASE_STORAGE_BUCKET` | `<project-id>.firebasestorage.app` |
| `FIREBASE_MESSAGING_SENDER_ID` | Sender ID from Firebase project settings |
| `FIREBASE_APP_ID` | App ID from Firebase project settings |
| `FIREBASE_MEASUREMENT_ID` | Analytics measurement ID (e.g., `G-XXXXXXXXXX`) |

### How to get Firebase credentials

1. Go to the [Firebase Console](https://console.firebase.google.com).
2. Create a new project (or open an existing one).
3. Click **Add app** → choose **Web** (`</>`).
4. Register your app. Firebase will display the config object.
5. Copy each value into your `.env`.
6. Enable **Google Sign-In** under **Authentication → Sign-in method**.

> Firebase integration is **optional for local development**. If Firebase variables are missing or invalid, Google Sign-In will not work, but email/password login will still function normally.

---

## Twilio Configuration (WhatsApp Notifications)

Twilio sends automated WhatsApp messages when sessions are scheduled, rescheduled, or updated.

| Variable | Description |
| :--- | :--- |
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID (found in the Twilio Console) |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token (found in the Twilio Console) |
| `TWILIO_WHATSAPP_FROM` | Your Twilio WhatsApp sender number, e.g. `whatsapp:+14155238886` |

These three variables are commented out in `.env.example` because WhatsApp notifications are **optional**.

### How to set up Twilio

1. Create a free account at [twilio.com](https://www.twilio.com).
2. In the Twilio Console, find your **Account SID** and **Auth Token** on the dashboard.
3. Activate the **WhatsApp Sandbox** under **Messaging → Try it out → Send a WhatsApp message**.
4. Note the sandbox number (e.g., `+14155238886`) and set it as `TWILIO_WHATSAPP_FROM`.
5. Add the `whatsapp:` prefix: `TWILIO_WHATSAPP_FROM=whatsapp:+14155238886`.

> Users must join the Twilio sandbox by sending a join code to the sandbox number before they can receive messages in development mode.

---

## Email Configuration (Gmail SMTP)

The project uses Gmail SMTP to send session notification emails. Django's `EMAIL_*` settings are configured in `updated_skill_exchange_network/settings.py`.

To enable email notifications, add the following to `settings.py` (or to `.env` if your settings file reads from it):

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-gmail-address@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # NOT your Google account password
```

### Creating a Gmail App Password

Google requires an **App Password** (not your regular password) for SMTP access:

1. Enable **2-Step Verification** on your Google account.
2. Go to **Google Account → Security → App passwords**.
3. Select app: **Mail**, device: **Other (custom name)**, give it a name.
4. Copy the generated 16-character password.
5. Use it as `EMAIL_HOST_PASSWORD`.

---

## Database Configuration

By default the project uses **SQLite**, which requires no configuration:

```python
# settings.py (default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For **PostgreSQL** in production, replace the `DATABASES` dict:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skill_exchange_db',
        'USER': 'postgres',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Install the PostgreSQL adapter:

```bash
pip install psycopg2-binary
```

---

## Production Checklist

Before deploying to a production server:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set `ALLOWED_HOSTS` in `settings.py` to your domain
- [ ] Use a strong, randomly generated `SECRET_KEY`
- [ ] Switch to PostgreSQL (or another production-grade database)
- [ ] Configure a reverse proxy (Nginx, Apache) in front of `gunicorn`
- [ ] Serve static files via `python manage.py collectstatic` + a CDN or web server
- [ ] Use HTTPS (TLS certificate via Let's Encrypt)
- [ ] Store all secrets in environment variables, not in source code
