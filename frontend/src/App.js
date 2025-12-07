import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Quiz from "./pages/Quiz";
import MyQuizzes from "./pages/MyQuizzes";
import CreateQuiz from "./pages/CreateQuiz";
import MyResults from "./pages/MyResults";
import Results from "./pages/Results"; // <-- add

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/" replace />;
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz/:id" element={<Quiz />} />
        <Route path="/results" element={<Results />} /> {/* immediate result */}
        <Route path="/results/:attemptId" element={<PrivateRoute><Results /></PrivateRoute>} /> {/* historical */}
        <Route path="/my-results" element={<PrivateRoute><MyResults /></PrivateRoute>} />
        <Route path="/my-quizzes" element={<PrivateRoute><MyQuizzes /></PrivateRoute>} />
        <Route path="/create-quiz" element={<PrivateRoute><CreateQuiz /></PrivateRoute>} />
        <Route path="/edit-quiz/:id" element={<PrivateRoute><CreateQuiz /></PrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
