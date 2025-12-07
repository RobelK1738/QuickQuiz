import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getQuizById, submitQuiz } from "../services/api";
import QuestionCard from "../components/QuestionCard";

function Quiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState([]); // answers only

  useEffect(() => {
    getQuizById(id).then((res) => {
      setQuiz(res.data);
      // initialize answers as empty strings for each question
      setAnswers(Array(res.data.questions.length).fill(""));
    });
  }, [id]);

  // update answer at specific question index
  const handleAnswer = (index, answer) => {
    setAnswers((prev) => {
      const updated = [...prev];
      updated[index] = answer;
      return updated;
    });
  };

  const handleSubmit = async () => {
    try {
      // ✅ format answers to include question_id for backend
      const formattedAnswers = quiz.questions.map((q, idx) => ({
        question_id: q.id,
        answer: answers[idx],
      }));

      const res = await submitQuiz(id, formattedAnswers);
      navigate("/results", { state: res.data });
    } catch (err) {
      console.error("Submit error:", err.response?.data || err.message);
    }
  };

  if (!quiz) return <div className="p-6 text-center">Loading...</div>;

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-4 text-center">{quiz.title}</h2>
      <p className="text-gray-600 mb-6 text-center">{quiz.description}</p>

      <div className="space-y-6">
        {quiz.questions.map((q, idx) => (
          <QuestionCard
            key={q.id}
            question={q}
            index={idx}
            onAnswer={handleAnswer}
          />
        ))}
      </div>

      <div className="text-center mt-8">
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Submit Quiz
        </button>
      </div>
    </div>
  );
}

export default Quiz;
