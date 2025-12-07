import React, { useEffect, useState } from "react";
import { getMyQuizzes, deleteQuiz } from "../services/api";
import { useNavigate } from "react-router-dom";

function MyQuizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const navigate = useNavigate();

  const loadQuizzes = async () => {
    try {
      const res = await getMyQuizzes();
      setQuizzes(res.data);
    } catch (err) {
      console.error("Error loading quizzes:", err);
    }
  };

  useEffect(() => {
    loadQuizzes();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this quiz?")) {
      await deleteQuiz(id);
      loadQuizzes();
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold">My Quizzes</h2>
        <button
          onClick={() => navigate("/create-quiz")}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + New Quiz
        </button>
      </div>
      {quizzes.length === 0 ? (
        <p className="text-gray-500">You haven’t created any quizzes yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {quizzes.map((quiz) => (
            <div
              key={quiz.id}
              className="border p-4 rounded shadow-sm bg-white flex flex-col justify-between"
            >
              <div>
                <h3 className="font-semibold text-xl">{quiz.title}</h3>
                <p className="text-gray-600">{quiz.description}</p>
              </div>
              <div className="flex justify-end mt-3 space-x-2">
                <button
                  onClick={() => navigate(`/edit-quiz/${quiz.id}`)}
                  className="bg-yellow-400 hover:bg-yellow-500 text-black px-3 py-1 rounded"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(quiz.id)}
                  className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MyQuizzes;
