# QuickQuiz Backend

Backend for **QuickQuiz**, a lightweight challenge/quiz web app where authenticated users create short quizzes and anyone can play them.

This service is implemented according to the QuickQuiz 1-Pager, PRD, UI Design, Design Doc, and Testing Plan. It provides the core MVP required by the course:

- Authenticated users can **create**, **view**, and **delete** their own quizzes.
- All users can **list** public quizzes, **play** quizzes, **submit** answers, see their **score**, and **reveal** correct answers.

---

## 🚀 Deployment & Live App

QuickQuiz Backend is live and publicly accessible!

### 🌐 Live URL

- **Backend (FastAPI + Render):** [https://quickquizbackend.onrender.com/](https://quickquizbackend.onrender.com/)

### ⚙️ Deployment Details

- **Backend** hosted on **Render** — deployed directly from the `backend/` directory.  
  - Runs FastAPI via `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`.  
  - Uses a managed **PostgreSQL** database.  
  - Firebase Admin SDK configured via environment variable `FIREBASE_CREDENTIALS`.

---

## 1. Tech Stack

**`Runtime & Frameworks`**

- Python 3.11+ (tested with 3.11+)
- FastAPI – backend web framework
- Uvicorn – ASGI server
- SQLAlchemy – ORM
- SQLite – default local database (file-based)
- Firebase Admin SDK – verify Firebase Authentication ID tokens

**`Testing`**

- pytest
- FastAPI TestClient (Starlette + httpx)
- In-memory SQLite DB for isolated test runs

---

## 2. Project Structure

From the `backend` root:

```bash
backend/
├─ app/
│  ├─ main.py               # FastAPI app entrypoint
│  ├─ core/
│  │  ├─ config.py          # Settings (DB URL, Firebase config, etc.)
│  │  ├─ database.py        # SQLAlchemy engine, SessionLocal, Base
│  │  └─ auth.py            # Firebase auth verification + dependency helpers
│  ├─ models/
│  │  └─ models.py          # SQLAlchemy models: User, Quiz, Question, Attempt
│  ├─ schemas/
│  │  └─ quizzes.py         # Pydantic schemas for requests/responses
│  ├─ routers/
│  │  └─ quizzes.py         # Quiz CRUD + play/submit endpoints
│  └─ __init__.py
├─ tests/
│  ├─ conftest.py           # Test app + test DB + auth overrides
│  ├─ test_public_quizzes.py
│  ├─ test_quiz_create.py
│  ├─ test_my_quizzes_and_delete.py
│  └─ test_submit_scoring.py
├─ .env.example
├─ requirements.txt
└─ README.md
```

This layout is intentionally small and matches the one-week MVP scope.

---

## 3. Setup

### 3.1. Prerequisites

- Python 3.11+ installed
- Git installed
- A Firebase project with:
  - Web app configured
  - Firebase Authentication enabled (Google sign-in)
  - A Service Account key with permissions to verify ID tokens (or Application Default Credentials)

### 3.2. Clone & Create Virtual Environment

From your workspace:

```bash
git clone <your-repo-url> backend
cd backend

python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# or: .venv\Scripts\activate     # Windows
```

### 3.3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.4. Environment Variables

Create a `.env` file in the `backend` root:

```env
# .env

# SQLite by default (local dev)
DATABASE_URL=sqlite:///./quickquiz.db

# (Optional) Different DB:
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/quickquiz

# Firebase project ID (for context / optional checks)
FIREBASE_PROJECT_ID=your-firebase-project-id

# Path to Firebase service account JSON (if not using GOOGLE_APPLICATION_CREDENTIALS)
# FIREBASE_CREDENTIALS=/absolute/path/to/serviceAccountKey.json
```

The backend will:

- Use `DATABASE_URL` for the SQLAlchemy engine.
- Initialize Firebase Admin via:
  - `GOOGLE_APPLICATION_CREDENTIALS`, or
  - Application Default Credentials, depending on your environment.

### 3.5. Firebase Service Account

1. In Firebase Console → **Project Settings → Service Accounts**.
2. Click **Generate new private key**, save JSON.
3. Export:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/serviceAccountKey.json"
```

This allows `firebase_admin.credentials.ApplicationDefault()` in `auth.py` to verify tokens.

No Firestore is used; persistence is handled with SQLAlchemy + SQLite.

---

## 4. Running the Server

From `backend` with your virtualenv active and `.env` ready:

```bash
uvicorn app.main:app --reload
```

- `--reload` enables hot reload.
- On startup, `Base.metadata.create_all(bind=engine)` will create tables if they don’t exist.
- API docs:
  - Swagger UI: <http://localhost:8000/docs>
  - ReDoc: <http://localhost:8000/redoc>

---

## 5. Authentication

QuickQuiz uses **Firebase ID tokens** for protected routes.

### 5.1. Client Flow

1. Frontend uses Firebase JS SDK for Google Sign-In.
2. Frontend calls `user.getIdToken()` to get an ID token.
3. Each protected request sends:

```http
Authorization: Bearer <FIREBASE_ID_TOKEN>
```

### 5.2. Backend Flow

In `app/core/auth.py`:

- `get_current_user`:
  - Uses `firebase_admin.auth.verify_id_token`.
  - Extracts `uid` & `name`.
  - Ensures a `User` row exists (`id = uid`, `name = name`).
  - Returns the `User` instance to the endpoint via dependency injection.

- `get_optional_user`:
  - Same as above, but returns `None` if token missing/invalid.
  - Used for endpoints that allow both anonymous and authenticated users.

If the token is invalid/missing where required → `401 Unauthorized`.

For Postman/local testing you can:

- Use a real ID token from a logged-in Firebase user, or
- Temporarily replace `get_current_user` with a fixed test user for local-only debugging (do not ship that).

---

## 6. API Endpoints

All main endpoints are under `/api`.

### 6.1. List Public Quizzes

```http
GET /api/quizzes
```

- Public.
- Returns list of all quizzes (for MVP, all quizzes are treated as visible).

**200 Response Example:**

```json
[
  {
    "id": 1,
    "title": "Intro CS Quiz",
    "description": "Warm-up questions",
    "creator_display_name": "Test User"
  }
]
```

---

### 6.2. List My Quizzes

```http
GET /api/quizzes/my
Authorization: Bearer <token>
```

- Requires auth.
- Returns quizzes created by the current user.

**200 Response Example:**

```json
[
  {
    "id": 3,
    "title": "My Networks Quiz",
    "description": "Quick TCP/IP check",
    "created_at": "2025-11-10T12:00:00Z"
  }
]
```

---

### 6.3. Create Quiz

```http
POST /api/quizzes
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Networks Warmup",
  "description": "Quick TCP/IP check",
  "questions": [
    {
      "text": "What does TCP stand for?",
      "correct_answer": "Transmission Control Protocol"
    },
    {
      "text": "Which layer is IP?",
      "correct_answer": "Network"
    }
  ]
}
```

**Rules:**

- `title` required (non-empty).
- `questions` required:
  - At least 1, at most 10.
  - Each with non-empty `text` and `correct_answer`.

**Responses:**

- `201 Created` – quiz summary with ID.
- `400 Bad Request` – validation errors.
- `401 Unauthorized` – if missing/invalid token.

---

### 6.4. Get Quiz Details

```http
GET /api/quizzes/{quiz_id}
```

- Public.
- Returns quiz metadata + questions for playing.

**200 Response Example:**

```json
{
  "id": 1,
  "title": "Networks Warmup",
  "description": "Quick TCP/IP check",
  "questions": [
    { "id": 10, "text": "What does TCP stand for?" },
    { "id": 11, "text": "Which layer is IP?" }
  ]
}
```

Correct answers are not exposed in this response.

---

### 6.5. Submit Answers

```http
POST /api/quizzes/{quiz_id}/submit
Content-Type: application/json

{
  "answers": [
    "transmission control protocol",
    " network "
  ]
}
```

**Behavior:**

- Matches each answer to the corresponding question:
  - Strips whitespace.
  - Compares case-insensitive.
- Missing or empty answers are incorrect.
- Returns:
  - Per-question correctness.
  - `score` and `total`.
  - Correct answers so users can see what they missed.

**200 Response Example:**

```json
{
  "score": 2,
  "total": 2,
  "results": [
    {
      "question": "What does TCP stand for?",
      "user_answer": "transmission control protocol",
      "correct_answer": "Transmission Control Protocol",
      "is_correct": true
    },
    {
      "question": "Which layer is IP?",
      "user_answer": " network ",
      "correct_answer": "Network",
      "is_correct": true
    }
  ]
}
```

**Errors:**

- `404 Not Found` – quiz does not exist.
- `400 Bad Request` – malformed payload.

---

### 6.6. Delete Quiz

```http
DELETE /api/quizzes/{quiz_id}
Authorization: Bearer <token>
```

**Rules:**

- Only the quiz creator can delete their quiz.
- Deletes associated questions (and any related attempts, if modeled).

**Responses:**

- `204 No Content` – success.
- `401 Unauthorized` – no/invalid token.
- `403 Forbidden` – caller is not quiz owner.
- `404 Not Found` – quiz not found.

---

## 7. Development Notes

### 7.1. Database

- Default: `sqlite:///./quickquiz.db`
- Tables auto-created via `Base.metadata.create_all(bind=engine)` at app startup.
- For schema changes during development:
  - Option 1: Drop `quickquiz.db` and restart.
  - Option 2: Manually adjust schema (sufficient for this course project).

### 7.2. Local Testing Without Firebase

For quick manual checks, you can (locally only):

- Temporarily change `get_current_user` to return a static user.
- Or use Postman with a real Firebase ID token from your frontend.

Make sure to keep production/commit-safe behavior (real verification) in `main` branches.

---

## 8. Testing Suite

All tests are written with `pytest` and live in `tests/`.

### 8.1. How to Run

From `backend` with `.venv` active:

```bash
pytest
```

This will:

- Spin up a FastAPI TestClient.
- Use an in-memory SQLite database.
- Override:
  - `get_db` → test database session.
  - `get_current_user` → deterministic fake user (no real Firebase calls).

### 8.2. What’s Covered

**`test_public_quizzes.py`**

- `GET /api/quizzes` returns empty list on fresh DB.
- (With created quizzes) returns visible quizzes.

**`test_quiz_create.py`**

- Successful quiz creation with valid payload.
- Rejects missing title.
- Enforces at least one question.
- Rejects empty question text / empty correct_answer.
- Guards overall request shape.

**`test_my_quizzes_and_delete.py`**

- `GET /api/quizzes/my` returns only quizzes by the current (fake) user.
- `DELETE /api/quizzes/{id}`:
  - Works for quiz owner.
  - (If you add) returns appropriate error for non-owner.

**`test_submit_scoring.py`**

- `GET /api/quizzes/{id}` returns quiz details correctly.
- `POST /api/quizzes/{id}/submit`:
  - Scores correct answers.
  - Is case-insensitive.
  - Trims whitespace.
  - Handles incorrect and missing answers as expected.

These tests jointly validate:

- Request/response schemas.
- Core business rules (ownership, validation).
- Scoring logic (a core part of the MVP).
- That wiring between routers, models, schemas, and auth overrides is correct.

### 8.3. Adding New Tests

If you extend QuickQuiz (attempt history, leaderboards, tags, etc.):

1. Add scenarios to the PRD & design.
2. Add or update endpoints.
3. Add corresponding tests in `tests/`:
   - Happy path.
   - Input validation.
   - Auth/permission checks.

---

## 9. Troubleshooting

**`no such table: users` or `no such table: quizzes`**

- Ensure startup code runs `Base.metadata.create_all(bind=engine)`.
- For tests: confirm the test DB initialization in `conftest.py` is executed before queries.

**`Invalid authentication credentials` (401)**

- Check `GOOGLE_APPLICATION_CREDENTIALS`.
- Ensure you’re sending a valid Firebase **ID token** in `Authorization: Bearer ...`.

**`Import/path issues`**

- Run commands from the `backend` directory.
- `app/` must contain `__init__.py`.
- Use `uvicorn app.main:app --reload` (not `python app/main.py`).

---

## 10. Alignment with QuickQuiz Docs

This backend matches the documented QuickQuiz stack and scope:

- Simple challenge/quiz model.
- Firebase-based authentication.
- Core CRUD + play/submit flows.
- Clean separation of config, auth, models, routers.
- Automated tests aligned with the Testing Plan and traceability matrix.

---

## 👨‍💻 Contributors

- **Robel Kebede** — Full Stack Developer
- **Trishma Garcon** - Project Manager
- **Xavier Green** - UI/UX and Front End Developer
- **Caleb Orr** - Back End Developer
- **Dalvin Ticha** - Test Engineer

---

## 📄 License

This project is licensed under the MIT License.
