import React from "react";
import { useNavigate } from "react-router-dom";

function QuizCard({ quiz }) {
  const navigate = useNavigate();

  return (
    <div className="border rounded-lg shadow-md p-5 hover:bg-blue-50 transition">
      <h3 className="text-xl font-semibold mb-2">{quiz.title}</h3>
      <p className="text-gray-600 mb-4">{quiz.description}</p>

      {quiz.latestAttempt?.attempted ? (
        <div className="text-center">
          <p className="text-sm text-gray-700 mb-2">
            You already completed this quiz.
            <br />
            Score:{" "}
            <strong>
              {quiz.latestAttempt.score} / {quiz.latestAttempt.total}
            </strong>
          </p>
          <button
            onClick={() =>
              navigate(`/results/${quiz.latestAttempt.attempt_id}`)
            }
            className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
          >
            View Results
          </button>
        </div>
      ) : (
        <button
          onClick={() => navigate(`/quiz/${quiz.id}`)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Start Quiz
        </button>
      )}
    </div>
  );
}

export default QuizCard;
