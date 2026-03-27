# Task Manager API

A production-ready REST API built with Flask, PostgreSQL, and JWT authentication. Supports full task management with secure user accounts — deployed live on Railway.

🔗 **Live API:** https://task-manager-api-production-944a.up.railway.app

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL (production), SQLite (local)
- **ORM:** SQLAlchemy
- **Auth:** JWT (PyJWT), bcrypt password hashing
- **Deployment:** Railway + Gunicorn

---

## Features

- User registration and login with hashed passwords
- JWT-based authentication on all task routes
- Full CRUD for tasks — create, read, update, delete
- Users can only access and modify their own tasks
- Persistent PostgreSQL database in production

---

## API Reference

### Auth

#### Register
```
POST /register
```
```json
{
  "email": "you@example.com",
  "password": "yourpassword"
}
```
**Response:** `201 Created`
```json
{ "message": "registered successfully" }
```

---

#### Login
```
POST /login
```
```json
{
  "email": "you@example.com",
  "password": "yourpassword"
}
```
**Response:** `200 OK`
```json
{ "token": "eyJhbGci..." }
```

---

### Tasks

All task routes require the header:
```
Authorization: Bearer <token>
```

#### Get all tasks
```
GET /tasks
```
**Response:** `200 OK`
```json
[
  { "id": 1, "title": "Learn Flask", "completed": false },
  { "id": 2, "title": "Deploy to Railway", "completed": true }
]
```

---

#### Create a task
```
POST /tasks
```
```json
{ "title": "My new task" }
```
**Response:** `201 Created`
```json
{ "id": 3, "title": "My new task", "completed": false }
```

---

#### Mark task as completed
```
PUT /tasks/<id>
```
**Response:** `200 OK`
```json
{ "id": 3, "title": "My new task", "completed": true }
```

---

#### Delete a task
```
DELETE /tasks/<id>
```
**Response:** `200 OK`
```json
{ "message": "Task deleted successfully" }
```

---

## Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/SiddhiGalada44/task-manager-api.git
cd task-manager-api
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///tasks.db
```

### 5. Run the server
```bash
python app.py
```

Server runs at `http://localhost:8000`

---

## Project Structure

```
task-manager-api/
├── app.py              # Flask app entry point
├── models.py           # SQLAlchemy database models
├── auth.py             # JWT and bcrypt helpers
├── routes/
│   ├── auth_routes.py  # /register and /login
│   └── task_routes.py  # CRUD task endpoints
├── Procfile            # Railway deployment config
├── requirements.txt
└── .env                # Local secrets (not committed)
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad request — missing or invalid fields |
| 401  | Unauthorized — missing or invalid token |
| 404  | Resource not found |
| 409  | Conflict — email already registered |
