import React, { useEffect, useState } from "react";
import { getPublicQuizzes, getMyLatestAttempt } from "../services/api";
import QuizCard from "../components/QuizCard";

function Home() {
  const [quizzes, setQuizzes] = useState([]);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const res = await getPublicQuizzes();
        const quizzes = res.data;

        // For each quiz, check if the logged-in user has an attempt
        const updated = await Promise.all(
          quizzes.map(async (quiz) => {
            try {
              const attemptRes = await getMyLatestAttempt(quiz.id);
              return { ...quiz, latestAttempt: attemptRes.data };
            } catch {
              return { ...quiz, latestAttempt: { attempted: false } };
            }
          })
        );

        setQuizzes(updated);
      } catch (err) {
        console.error("Failed to fetch quizzes:", err);
      }
    };

    fetchQuizzes();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold text-center mb-6">Available Quizzes</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {quizzes.map((quiz) => (
          <QuizCard key={quiz.id} quiz={quiz} />
        ))}
      </div>
    </div>
  );
}

export default Home;
