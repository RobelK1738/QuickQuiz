import React, { useState, useEffect } from "react";
import { createQuiz, getQuizById, updateQuiz } from "../services/api";
import { useNavigate, useParams } from "react-router-dom";

function CreateQuiz() {
  const navigate = useNavigate();
  const { id } = useParams();
  const editing = Boolean(id);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [questions, setQuestions] = useState([{ text: "", correct_answer: "" }]);

  useEffect(() => {
    if (editing) {
      getQuizById(id).then((res) => {
        setTitle(res.data.title);
        setDescription(res.data.description);
        setQuestions(res.data.questions);
      });
    }
  }, [id, editing]);

  const handleQuestionChange = (index, field, value) => {
    const updated = [...questions];
    updated[index][field] = value;
    setQuestions(updated);
  };

  const addQuestion = () => {
    setQuestions([...questions, { text: "", correct_answer: "" }]);
  };

  const removeQuestion = (index) => {
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const quizData = { title, description, questions };
    if (editing) await updateQuiz(id, quizData);
    else await createQuiz(quizData);
    navigate("/my-quizzes");
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-4">
        {editing ? "Edit Quiz" : "Create New Quiz"}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Title</label>
          <input
            type="text"
            className="w-full border px-3 py-2 rounded"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Description</label>
          <textarea
            className="w-full border px-3 py-2 rounded"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">Questions</label>
          {questions.map((q, index) => (
            <div
              key={index}
              className="border p-3 mb-3 rounded bg-gray-50 space-y-2"
            >
              <input
                type="text"
                className="w-full border px-3 py-2 rounded"
                placeholder="Question text"
                value={q.text}
                onChange={(e) =>
                  handleQuestionChange(index, "text", e.target.value)
                }
                required
              />
              <input
                type="text"
                className="w-full border px-3 py-2 rounded"
                placeholder="Correct answer"
                value={q.correct_answer}
                onChange={(e) =>
                  handleQuestionChange(index, "correct_answer", e.target.value)
                }
                required
              />
              <button
                type="button"
                onClick={() => removeQuestion(index)}
                className="text-sm text-red-600 hover:underline"
              >
                Remove Question
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={addQuestion}
            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
          >
            + Add Question
          </button>
        </div>

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          {editing ? "Save Changes" : "Create Quiz"}
        </button>
      </form>
    </div>
  );
}

export default CreateQuiz;
