# API Reference

The Skill Exchange Network exposes a lightweight JSON REST API at the `/api/` prefix. This API is used by the frontend via AJAX and can be consumed by any external client.

All JSON responses contain a `status` field (`"success"` or `"error"`) and a `message` field with a human-readable description.

---

## Base URL

```
http://127.0.0.1:8000/api/
```

---

## Authentication

Most API endpoints require the user to be **logged in** (session-based authentication). Unauthenticated requests to protected endpoints return an HTTP **302 redirect** to `/login/`.

---

## Endpoints

### `GET /api/health/`

Health check. Returns the API version and a list of all available endpoints.

**Authentication required**: No

**Response `200 OK`**
```json
{
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
}
```

---

### `GET /api/live-users/`

Returns platform-wide statistics. Used on the homepage to display live counters.

**Authentication required**: No

**Response `200 OK`**
```json
{
  "total_users": 120,
  "active_users": 115,
  "total_skills": 42,
  "total_exchanges": 87
}
```

---

### `GET /api/notifications/`

Returns notification counts for the currently authenticated user.

**Authentication required**: Yes

**Response `200 OK`**
```json
{
  "pending_requests": 3,
  "sent_requests": 1,
  "accepted_exchanges": 5,
  "total_notifications": 3
}
```

| Field | Description |
| :--- | :--- |
| `pending_requests` | Exchange requests waiting for *this user* to respond |
| `sent_requests` | Requests *this user* sent that are still pending |
| `accepted_exchanges` | Total active (accepted) exchanges this user is part of |
| `total_notifications` | Same as `pending_requests` — used for navbar badge |

---

### `POST /api/request-exchange/`

Send a skill-exchange request to a teacher. This is the AJAX equivalent of the HTML form at `/request-exchange/`.

**Authentication required**: Yes  
**Content-Type**: `application/json`

**Request body**
```json
{
  "teacher_id": 5,
  "skill_name": "Python Programming",
  "offering_skill": "Web Design",
  "preferred_time": "Weekends",
  "message": "I'd love to learn Python!"
}
```

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `teacher_id` | integer | Yes | ID of the user you want to learn from |
| `skill_name` | string | Yes | Exact name of the skill (must exist in the database) |
| `offering_skill` | string | Yes | What you will teach in return |
| `preferred_time` | string | Yes | When you prefer to meet |
| `message` | string | No | Optional personal note to the teacher |

**Response `200 OK`** (success)
```json
{
  "status": "success",
  "message": "Request sent successfully!"
}
```

**Error responses**

| HTTP Status | `message` | Cause |
| :--- | :--- | :--- |
| `400` | `"You cannot request exchange with yourself!"` | `teacher_id` matches the logged-in user |
| `400` | `"You already have a pending request with this teacher!"` | Duplicate pending request |
| `404` | `"Teacher not found!"` | `teacher_id` does not exist |
| `404` | `"Skill not found!"` | `skill_name` does not match any skill |
| `400` | *(exception message)* | Any other server error |

---

### `POST /api/exchanges/<exchange_id>/schedule/`

Schedule a date and time for an accepted exchange session. Only the **requester** or **receiver** of the exchange may call this endpoint.

**Authentication required**: Yes  
**Content-Type**: `application/json`

**URL parameter**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `exchange_id` | integer | ID of the `ExchangeRequest` to schedule |

**Request body**
```json
{
  "date": "2026-06-15",
  "time": "14:00"
}
```

| Field | Format | Description |
| :--- | :--- | :--- |
| `date` | `YYYY-MM-DD` | Date of the session |
| `time` | `HH:MM` | Time of the session (24-hour format) |

**Response `200 OK`** (success)
```json
{
  "status": "success",
  "message": "Session scheduled for 2026-06-15 at 14:00. Notification sent!",
  "exchange_id": 42,
  "date": "2026-06-15",
  "time": "14:00"
}
```

**Error responses**

| HTTP Status | `message` | Cause |
| :--- | :--- | :--- |
| `403` | `"You are not authorized to schedule this session!"` | Caller is not a participant |
| `404` | `"Exchange not found or not accepted yet!"` | Exchange does not exist or is not accepted |
| `400` | *(exception message)* | Any other server error |

---

## Error Format

All error responses follow this shape:

```json
{
  "status": "error",
  "message": "Human-readable description of the error."
}
```

---

## Notes

- The API uses **session-based authentication** (cookies), not token-based auth. If you are building an external client you will need to log in via the browser first, or extend the project to support token authentication.
- `POST /api/request-exchange/` and `POST /api/exchanges/<id>/schedule/` are decorated with `@csrf_exempt` because they receive JSON bodies from JavaScript code. Do not call these endpoints directly from forms without a CSRF token.
