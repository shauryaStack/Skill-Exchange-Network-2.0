# Skill Exchange Network - Detailed Project Breakdown

Welcome to the **Detailed Developer and Non-Developer Guide** for the Skill Exchange Network project! This document explains exactly how the project is built, the role of each file, and what every piece of code does in simple terms.

Whether you are a coder looking to understand the mechanics, or a non-coder trying to grasp how the platform operates behind the scenes, this guide is for you!

---

## 🏗️ 1. The Big Picture (How it all connects)

Think of this project as a restaurant:
- **Models (`models.py`)**: The storage room and ingredients. This tells us what data we have (e.g., Users, Skills, Requests).
- **Views (`views.py`)**: The chef. They take requests from the waiters, grab ingredients from the storage (database), and prepare the meal (webpage).
- **URLs (`urls.py`)**: The waiters. When you enter a web address (like `/profile/`), the URL system takes your order and hands it to the right chef (View).
- **Templates (HTML Files)**: The presentation. This is the plate that is served to the user (the shiny buttons, colors, and layout).
- **Utils (`utils.py`)**: Specialized helpers, like a delivery driver who sends out Emails and WhatsApp messages.

---

## 📂 2. Core App Files Explained

The vast majority of the magic happens in a folder called `core`. Let's look inside:

### 🗄️ `core/models.py` (The Database Blueprint)
This file defines what information is stored in the database.

- **`User` class**: Represents a person on the platform. It takes Django's standard user (which covers login/password) and adds extra details like their `phone` number, `division`, and `firebase_uid` (if they log in via Google).
- **`Skill` class**: A list of all skills that can be taught or learned (e.g., Python, Piano, Content Writing). Every skill is uniquely named.
- **`UserTeaches` class**: The connector. It links a `User` to a `Skill`. It also stores *how proficient* the user is, their *availability*, and any special *notes*. For example: "John teaches Python at an Expert level."
- **`ExchangeRequest` class**: When someone asks another person to teach them. It keeps track of the *requester*, the *receiver* (teacher), the requested *skill*, what is offered in return, the chosen meeting platform (Google Meet/Teams), and the current *status* (Pending, Accepted, Rejected).

### 👨‍🍳 `core/views.py` (The Brain of the Application)
This massive file contains all the functions that process user actions and show web pages. Here are the key "functions" (actions) inside it:

**Authentication (Logging In & Out):**
- **`login_view`**: Checks a user's email and password to safely log them in.
- **`firebase_login`**: A special login handle for Google Sign-In using Firebase.
- **`register_view`**: Shows the sign-up page. When submitted, it creates the new user account and saves the skills they want to teach.
- **`logout_view`**: Safely logs the user out.

**Main Pages:**
- **`index`**: Loads the homepage and shows overall platform statistics.
- **`profile_view`**: Loads the user's dashboard. It pulls all the user's taught skills, incoming requests, and active sessions from the database, then sends them to `profile.html`.
- **`browse_view`**: Shows all available skills on the platform so users can find what they want to learn.
- **`match_view`**: After you click a skill in Browse, this view finds and lists all the users who teach that specific skill.
- **`sessions_view`**: Shows a list of accepted meetings/sessions (both teaching and learning).

**Exchange Requests:**
- **`request_exchange`**: Sends a "Can you teach me?" request to another user.
- **`accept_exchange` & `reject_exchange`**: Allows a teacher to say "Yes!" or "No thanks" to incoming requests.

**Skill Management:**
- **`add_skill`**: Lets a registered user add another skill to their profile.
- **`remove_skill`**: Lets a user delete a skill they no longer want to teach.

**Session Management:**
- **`reschedule_session`**: Allows users to change the promised date and time of an accepted skill exchange.

### 🗺️ `core/urls.py` (The Map)
This file connects a web link (like `yoursite.com/register/`) to the specific python function in `views.py` that should handle it. 
It says: "If a user goes to `/browse/`, trigger the `browse_view` function."

It also defines `api/` routes here, which are used by Javascript to talk to the server quietly in the background without refreshing the page.

### ✉️ `core/utils.py` (The Messenger)
This is a helper file designed strictly to handle notifications. It separates the messy communication code away from the main logic.

- **`send_session_email`**: Sends an automated email using Gmail to users.
- **`send_whatsapp_to_user`**: Connects to an external service called "Twilio" to shoot an automated WhatsApp message directly to a user's phone.
- **`send_schedule_notification`**: Used when a session date is set or changed. It finds out who the "partner" is and texts/emails them the new date automatically.
- **`send_meeting_link_notification`**: Texts/emails the user when a Google Meet or Microsoft Teams link has been generated.

### 🔌 `core/api_views.py` (The Background Worker)
While `views.py` handles loading entire web pages, `api_views.py` handles tiny data requests behind the scenes.
For example, if the website wants to check how many notifications a user has without reloading the whole page, it talks to a small function here.

### 👮 `core/admin.py` (The Manager)
This registers the application's data models (`User`, `Skill`, `ExchangeRequest`) with Django's built-in Admin Panel. This allows the website owner to visit `/admin/` and manually edit records, ban users, or add new skills through a user-friendly interface.

---

## 🎨 3. The Frontend (What the user sees)
Inside `core/templates/core/`, there are HTML files. These are the "outfits" the code wears.

- **`base.html`**: The skeleton of every page. It holds the top navigation bar and the footer. All other pages are injected into the middle of this file so you don't have to rewrite the navigation bar on every page.
- **`index.html`**: The beautiful homepage with statistics and a welcoming title.
- **`login.html` & `register.html`**: The forms users fill out.
- **`browse.html`**: The grid of skill cards you can click through.
- **`profile.html`**: Your personal command center, showing your notifications, skills, and data.

---

## 🚀 How a "Skill Exchange" Actually Works (A Simple Flow)

1. **Emma** wants to learn **Python**. She visits the `/browse/` page (`browse_view` is called).
2. She clicks "Python". The website takes her to `/match/?skill_id=5` (`match_view` runs, looking for Python teachers).
3. She sees **John** listed as a teacher. She clicks "Request".
4. The system runs the `request_exchange` function. A new `ExchangeRequest` record is created in the database.
5. John logs in and checks his `/profile/`. The `profile_view` loads all his incoming `ExchangeRequest`s from the database.
6. John clicks "Accept". The system runs the `accept_exchange` function, changing the request status from 'Pending' to 'Accepted'.
7. John schedules a date. The `reschedule_session` function updates the date in the database.
8. The `send_schedule_notification` in `utils.py` instantly sends an email and WhatsApp message to Emma saying "John scheduled your Python class!"

---

## 🎯 Summary for Non-Coders
The site uses a powerful, secure foundation called **Django**. Django acts as the middleman between what you visually click on (HTML/CSS) and where your information is securely stored forever (the SQL Database). The project is deeply modular — meaning the database, the page generation, and the messaging systems all live in their own separate neat files so we can change one without breaking the others.

## 💻 Summary for Coders
This project follows a classic Monolithic MTV (Model-Template-View) architecture using Django. It relies on standard ORM relations including a custom through-model (`UserTeaches`) for capturing extra many-to-many metadata. Background operations like Web APIs and external dependencies (Firebase, Twilio, SMTP) are abstracted out into utility layers to keep the core views clean.

*Document beautifully crafted for everyone to understand!*
