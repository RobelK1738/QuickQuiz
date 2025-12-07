# QuickQuiz Frontend

This is the **React frontend** for the QuickQuiz application — a lightweight and interactive quiz platform that integrates with the FastAPI backend. It handles user authentication, quiz display, quiz submissions, and result visualization.

---

## 🚀 Features

- 🧭 **Routing** with React Router (Home, Quiz, Results, etc.)
- 📋 **Take quizzes** fetched from the backend
- 📊 **View quiz results** after submission
- 👤 **User authentication** integrated with Firebase
- 🔒 **Access control** — users can only see or attempt their own quizzes
- 💾 **Axios API layer** for consistent backend communication
- 🎨 **Tailwind CSS** for clean, responsive design

---

## 🚀 Deployment & Live App

QuickQuiz Frontend is live and publicly accessible!

### 🌐 Live URLs

- **Frontend (React + Vercel):** [https://quickquizfrontend.vercel.app/](https://quickquizfrontend.vercel.app/)

### ⚙️ Deployment Details

- **Frontend** hosted on **Vercel** — automatically deployed from the `frontend/` directory.  
  - Runs the React build with Tailwind styling.  
  - Connected to Firebase for authentication.

---

## 🧩 Directory Structure

```text
frontend/
├── src/
│   ├── components/          # Reusable UI components (e.g. QuestionCard, Navbar)
│   ├── pages/               # Top-level route views (Home, Quiz, Results, etc.)
│   ├── services/            # API utilities (Axios setup, endpoints)
│   ├── App.js               # App routing and layout
│   ├── index.js             # React entry point
│   └── index.css            # Tailwind base styles
├── public/
│   ├── index.html
│   └── favicon.ico
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

---

## ⚙️ Installation

Make sure your backend is running first (`cd backend && ./runBackend.sh`), then set up the frontend.

```bash
cd frontend
./runFrontend.sh
```

Then visit [http://localhost:3000](http://localhost:3000).  
The frontend will automatically connect to your backend running on `http://127.0.0.1:8000/api`.

---

## 🔌 API Integration

All API requests are made through a centralized Axios instance in `src/services/api.js`.

Example endpoints:

```js
export const getQuizById = (id) => api.get(`/quizzes/${id}`);
export const submitQuiz = (id, answers) =>
  api.post(`/quizzes/${id}/submit`, { answers });
export const getMyLatestAttempt = (id) =>
  api.get(`/quizzes/${id}/my-latest-attempt`);
```

This design ensures consistent headers, error handling, and authentication across all API calls.

---

## 🔐 Firebase Authentication

Firebase is used for user authentication.  
Users can sign in with Google or Email/Password, and their JWT token is attached to API requests for validation.

Make sure you have a valid `.env` file in the frontend directory:

```text
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_BACKEND_URL=http://127.0.0.1:8000/api
```

---

## 🎨 Styling

The frontend uses **Tailwind CSS** for a clean, modern design.

Tailwind is integrated via `postcss` and automatically applied during builds.  
Custom components (buttons, cards, containers) follow a consistent, mobile-friendly layout.

---

## 🧪 Testing

For local testing, ensure both servers are running:

```bash
# Terminal 1
cd backend && ./runBackend.sh

# Terminal 2
cd frontend && npm start
```

Then open [http://localhost:3000](http://localhost:3000).  
Login, start a quiz, submit answers, and view results!

---

## 🧰 Build for Production

```bash
npm run build
```

This creates a production-ready build in the `build/` folder.

To serve the production build locally, use a package like **serve**:

```bash
npm install -g serve
serve -s build
```

Then visit [http://localhost:5000](http://localhost:5000).

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
