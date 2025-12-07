# QuickQuiz

QuickQuiz is a **full-stack quiz application** built with **FastAPI (backend)** and **React (frontend)**.  
It allows users to create, take, and manage quizzes while tracking their progress and performance.  
The system supports **user authentication**, **quiz attempt tracking**, and **score evaluation**.

---

## 🧠 Overview

- **Backend**: FastAPI + SQLAlchemy + Firebase Authentication
- **Frontend**: React + Tailwind CSS + Axios
- **Database**: SQLite (development) or PostgreSQL (production-ready)
- **Auth**: Firebase JWT tokens integrated with FastAPI dependency
- **API Communication**: RESTful JSON endpoints

---

## 🚀 Deployment & Live App

QuickQuiz is live and publicly accessible!

### 🌐 Live URLs

- **Frontend (React + Vercel):** [https://quickquizfrontend.vercel.app/](https://quickquizfrontend.vercel.app/)
- **Backend (FastAPI + Render):** [https://quickquizbackend.onrender.com/](https://quickquizbackend.onrender.com/)

### ⚙️ Deployment Details

- **Frontend** hosted on **Vercel** — automatically deployed from the `frontend/` directory.  
  - Runs the React build with Tailwind styling.  
  - Connected to Firebase for authentication.

- **Backend** hosted on **Render** — deployed directly from the `backend/` directory.  
  - Runs FastAPI via `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`.  
  - Uses a managed **PostgreSQL** database.  
  - Firebase Admin SDK configured via environment variable `FIREBASE_CREDENTIALS`.

### 🔗 Connection

The frontend communicates with the backend using the API base URL:

```js
baseURL: "https://quickquizbackend.onrender.com/api"
```

All requests are authenticated using Firebase ID tokens attached in the Authorization header.

---

## 📁 Project Structure

```text
QuickQuiz/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── main.py          # FastAPI entrypoint
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── routers/         # API endpoints (auth, quizzes, users)
│   │   ├── schemas.py       # Pydantic models
│   │   ├── database.py      # DB session + engine setup
│   │   ├── dependencies.py  # Firebase + auth verification
│   │   └── utils.py         # Helper utilities
│   ├── .env.example
│   ├── requirements.txt
│   ├── runBackend.sh        # Easy backend startup script
│   └── README_backend.md
│
├── frontend/                # React frontend app
│   ├── src/
│   │   ├── components/      # UI components (QuizCard, Navbar, etc.)
│   │   ├── pages/           # Page views (Home, Quiz, Results)
│   │   ├── services/        # Axios-based API calls
│   │   ├── hooks/           # Custom hooks (e.g., useAuth)
│   │   ├── App.js           # Routing setup
│   │   └── index.js         # Entry point
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── README_frontend.md
│
└── README.md                # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/RobelK1738/QuickQuiz.git
cd QuickQuix
```

### 2. Backend Setup

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
./runBackend.sh
```

Ensure your `.env` file is configured:

```text
DATABASE_URL=sqlite:///./quiz.db
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

The backend runs on [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 3. Frontend Setup

```bash
cd ../frontend
./runFrontend.sh
```

Frontend runs at [http://localhost:3000](http://localhost:3000).

Ensure `.env` in `frontend/` includes:

```text
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_BACKEND_URL=http://127.0.0.1:8000/api
```

---

## 🧩 Key Features

### 🧠 Quizzes

- Create and manage quizzes with multiple questions.
- Public/private quiz visibility options.
- Automatic scoring upon submission.

### 👤 User System

- Firebase authentication (Google or Email/Password).
- Secure access via JWTs.
- Personalized quiz history and attempt tracking.

### 📊 Attempts & Results

- Users can attempt each quiz only once.
- See past attempts and detailed results.
- Quiz results include total score and per-question review.

### 💅 UI/UX

- Built with **React** + **Tailwind CSS**.
- Mobile-responsive design.
- Clean, simple dashboard for quiz browsing and results viewing.

---

## 🔌 API Overview

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/quizzes` | List all public quizzes |
| `GET` | `/api/quizzes/{id}` | Get quiz details |
| `POST` | `/api/quizzes/{id}/submit` | Submit quiz answers |
| `GET` | `/api/quizzes/{id}/my-latest-attempt` | Fetch latest attempt for logged-in user |
| `DELETE` | `/api/quizzes/{id}` | Delete quiz (only by creator) |
| `GET` | `/api/users/me` | Get current user profile |

---

## 🧪 Testing

Run backend tests:

```bash
pytest
```

Run frontend tests (if configured):

```bash
npm test
```

---

## 🧑‍💻 Authors

- **Robel Melaku** — Full Stack Developer
  📧 [robel.kebede@bison.howard.edu]
- **Trishma Garcon** - Project Manager
  📧 [Trishma.Garcon@bison.howard.edu]
- **Xavier Green** - UI/UX and Front End Developer
  📧 [Xavier.Green@bison.howard.edu]
- **Caleb Orr** - Back End Developer
  📧 [Caleb.Orr@bison.howard.edu]
- **Dalvin Ticha** - Test Engineer
  📧 [dalvin.ticha@bison.howard.edu]

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 💬 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Firebase](https://firebase.google.com/)
