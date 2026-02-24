# 🔁 Skill Exchange Network: Peer-to-Peer Learning Platform
Skill Exchange Network is an interactive web application designed to connect users so they can teach and learn skills from one another. Instead of paying for courses, this platform leverages a collaborative barter system where users exchange their knowledge—connecting someone who wants to learn coding with someone who wants to learn a new language, for example.

## 🚀 Project Overview
This project was developed to create a collaborative and accessible educational ecosystem. It uses a robust scheduling and notification system to manage online learning sessions seamlessly between users.

### Key Features:
- **Interactive UI**: A sleek "Minimalist Light Mode" design built with responsive HTML/CSS for a seamless, distraction-free user experience.
- **Skill Browsing**: A categorized "Browse Skills" system making it easy to find mentors for specific topics (e.g., Content Writing, Programming, Design).
- **Session Scheduling**: Integrated session management with the ability to schedule and manage online teaching sessions (supports Google Meet and Microsoft Teams links).
- **Multi-Channel Notifications**: Automated session alerts, reminders, and updates delivered via Email (Gmail SMTP) and WhatsApp (Twilio API).
- **Secure Authentication**: Robust user login and profile management powered by Django Authentication and Firebase.

## 🛠️ Tech Stack
- **Backend/Framework**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS, Django Templates
- **Authentication**: Django Auth & Firebase
- **Notifications**: Twilio API (WhatsApp), Gmail SMTP (Email)
- **Database**: SQLite / PostgreSQL

## 📊 The Core Logic
The application operates on a reciprocal skill-sharing model. Users build profiles detailing what they can teach (Offerings) and what they want to learn (Requests).

**Match & Learn = Browse Peers + Request Session + Automated Scheduling**

### User Journey Breakdown:

| Stage | User Action | System Response |
| :--- | :--- | :--- |
| **Profile Setup** | User lists Offered & Requested Skills | Profile becomes discoverable in the network |
| **Discovery** | Browse categories (e.g., via `/browse/`) | Filters and displays relevant skill cards |
| **Scheduling** | Request or Accept a session | Generates meeting links (Google Meet/Teams) |
| **Notifications** | Session gets booked or updated | Sends instant WhatsApp and Email alerts |

## 💻 Installation & Setup
To run this project locally, follow these steps:

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/your-username/skill-exchange-network.git
   cd updated_skill_exchange_network
   ```

2. **Set Up Virtual Environment & Dependencies**:
   Ensure you have a `requirements.txt` file, then run:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**: 
   Create a `.env` file in the root directory and add your credentials (e.g., Twilio keys, Email SMTP settings, Firebase config, Django Secret Key).

4. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Launch the Application**:
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` in your browser to start exchanging skills!
