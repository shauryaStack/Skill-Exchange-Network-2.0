# User Guide

This guide explains every feature available to end users of the Skill Exchange Network platform.

---

## Creating an Account

1. Navigate to **http://127.0.0.1:8000/register/** (or the hosted URL).
2. Fill in:
   - **First Name** and **Last Name**
   - **Email address** — used as your login identifier
   - **Password**
   - **Division / Department** (optional)
   - **Phone number** (optional, used for WhatsApp notifications)
   - **Skills you can teach** — select from the skill list; you can add more later
3. Click **Register**. Your account is created and you are automatically logged in.

**Alternatively**, click **Sign in with Google** on the login page to use your Google account via Firebase. A new profile is created automatically on first sign-in.

---

## Logging In and Out

- **Login**: Go to `/login/`, enter your email and password, and click **Login**.
- **Google Sign-In**: Click **Sign in with Google** on the login page.
- **Logout**: Click your name or the **Logout** link in the navigation bar.

---

## Your Profile Dashboard

After logging in, visit `/profile/` to access your personal dashboard. The dashboard shows:

| Section | Description |
| :--- | :--- |
| **My Skills** | Skills you currently offer to teach |
| **Incoming Requests** | Requests from other users asking you to teach them |
| **Sent Requests** | Requests you have sent to other teachers |
| **Active Sessions** | Accepted exchanges with scheduled or pending meeting details |

### Adding a Skill

1. On your profile page, click **Add Skill**.
2. Choose a skill from the dropdown.
3. Set your **proficiency level** (Beginner / Intermediate / Advanced / Expert).
4. Enter your **availability** (e.g., "Weekdays evenings", "Flexible").
5. Add optional **notes** about your teaching style.
6. Click **Save**.

### Removing a Skill

Click the **Remove** button next to any skill in the "My Skills" section. This will permanently remove that teaching listing.

---

## Browsing Skills

Visit `/browse/` to see all skills available on the platform.

- Skills are organised by **category** (e.g., Programming, Design, Languages).
- Use the category filters to narrow your search.
- Click any skill card to see which users teach that skill.

---

## Requesting a Skill Exchange

1. From the Browse page, click a skill category and then a specific skill.
2. You are taken to `/match/?skill_id=<id>`, showing a list of teachers.
3. Review each teacher's **proficiency**, **availability**, and **notes**.
4. Click **Request Exchange** on the teacher you want.
5. Fill in the request form:
   - **Offering skill** — what you will teach in return
   - **Preferred time** — when you would like to meet
   - **Message** — optional personal note to the teacher
6. Click **Send Request**. The teacher receives a notification.

> A pending request already exists if you have already sent an unanswered request to the same teacher for the same skill.

---

## Managing Incoming Requests (Teachers)

When someone requests you as a teacher, you will see the request on your **Profile** page under **Incoming Requests**.

| Action | What it does |
| :--- | :--- |
| **Accept** | Marks the request as `accepted`. Both users receive an email and WhatsApp notification. |
| **Reject** | Marks the request as `rejected`. The requester is notified. |

---

## Scheduling a Session

Once a request is accepted, either participant can schedule the session:

1. Go to `/sessions/` or find the exchange in your Profile.
2. Click **Schedule Session** on the exchange card.
3. Pick a **date** and **time**.
4. Click **Save**. The other participant receives an email and WhatsApp notification with the schedule.

---

## Adding a Meeting Link

After scheduling:

1. Generate a meeting link in **Google Meet** or **Microsoft Teams**.
2. Return to your session in `/sessions/` or on your Profile.
3. Click **Add Meeting Link**.
4. Paste the link, select the platform, and click **Save**.
5. Both participants are notified with the link.

---

## Notifications

The platform sends automated notifications via:

- **Email** — delivered to the email address on your account
- **WhatsApp** — sent to the phone number on your account (requires Twilio to be configured)

You receive a notification when:

- Someone sends you an exchange request
- Your request is accepted or rejected
- A session is scheduled or rescheduled
- A meeting link is added

---

## Viewing Active Sessions

Visit `/sessions/` to see all of your active (accepted) exchanges, including:

- The skill being exchanged
- Your partner's name
- Scheduled date and time (if set)
- The meeting link (if added)
- Current status

---

## Account Settings

You can update your profile information from the Profile dashboard, including your phone number and division.

---

## Tips for a Great Exchange

- **Be specific** in your "offering skill" — it helps the teacher understand what they'll receive in return.
- **Set your availability** clearly on your skill listings so partners can coordinate easily.
- **Add a personal message** when requesting — teachers are more likely to accept requests with context.
- **Schedule promptly** after a request is accepted to keep momentum going.
