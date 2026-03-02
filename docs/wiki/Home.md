# 🔁 Skill Exchange Network — Wiki

Welcome to the official wiki for **Skill Exchange Network 2.0**, a peer-to-peer learning platform that connects people who want to teach with people who want to learn — all through a collaborative barter system.

---

## 📑 Wiki Pages

| Page | Description |
| :--- | :--- |
| [Installation & Setup](Installation-and-Setup.md) | How to clone, configure, and run the project locally |
| [Architecture](Architecture.md) | System design, data models, and file structure |
| [User Guide](User-Guide.md) | How to use every feature of the platform |
| [API Reference](API-Reference.md) | REST API endpoints, request/response formats |
| [Configuration](Configuration.md) | Environment variables and third-party integrations |
| [Contributing](Contributing.md) | How to contribute code, report bugs, and suggest features |

---

## 🚀 Project Overview

Skill Exchange Network is an interactive Django web application where users can:

- **Teach** skills they know
- **Learn** skills from others
- **Schedule** live sessions via Google Meet or Microsoft Teams
- **Receive** automated notifications via Email and WhatsApp

Instead of paying for courses, users barter their expertise — someone who can code teaches programming, and in return learns a language, design skill, or anything else the other person offers.

---

## 🛠️ Tech Stack at a Glance

| Layer | Technology |
| :--- | :--- |
| Backend / Framework | Django 4.2+ (Python) |
| Frontend | HTML5, Vanilla CSS, Django Templates |
| Authentication | Django Auth + Firebase (Google Sign-In) |
| Notifications | Gmail SMTP (email) + Twilio API (WhatsApp) |
| Database | SQLite (development) / PostgreSQL (production) |
| REST API | Django REST Framework |

---

## ⚡ Quick Start

```bash
git clone https://github.com/shauryapradhan546/Skill-Exchange-Network-2.0.git
cd Skill-Exchange-Network-2.0
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
python manage.py migrate
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

For the full setup guide, see [Installation & Setup](Installation-and-Setup.md).

---

## 🗺️ Feature Map

```
/ (Home)            — Platform stats and welcome page
/register/          — Create a new account
/login/             — Log in (email/password or Google via Firebase)
/profile/           — Personal dashboard: skills, requests, sessions
/browse/            — Browse all available skills by category
/match/             — View teachers for a chosen skill
/sessions/          — Manage active learning sessions
/admin/             — Django admin panel (staff only)
/api/               — JSON REST API
```

---

## 📜 License

This project is licensed under the terms in the [LICENSE](../../LICENSE) file.
