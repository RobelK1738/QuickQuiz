import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { getAttempt } from "../services/api";

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const { attemptId } = useParams();
  const [data, setData] = useState(location.state || null);
  const [loading, setLoading] = useState(!location.state && !!attemptId);

  useEffect(() => {
    const fetchById = async () => {
      if (!location.state && attemptId) {
        try {
          const res = await getAttempt(attemptId);
          const attempt = res.data || {};

          const resultsArray = Array.isArray(attempt.results)
            ? attempt.results
            : [];

          setData({
            attempt_id: attempt.attempt_id ?? attempt.id ?? Number(attemptId),
            quiz_id: attempt.quiz_id ?? attempt.quizId ?? null,
            quiz_title: attempt.quiz_title,
            score: attempt.score,
            total: attempt.total,
            results: resultsArray.map((r) => ({
              question: r.question || "Unknown question",
              user_answer: r.user_answer ?? "",
              correct_answer: r.correct_answer ?? "",
              is_correct: r.is_correct ?? r.correct ?? false,
            })),
            created_at: attempt.created_at,
          });
        } catch (e) {
          console.error("Error fetching attempt:", e);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchById();
  }, [attemptId, location.state]);

  if (loading) return <div className="p-6 text-center">Loading...</div>;
  if (!data) return <div className="p-6 text-center">No result to display.</div>;

  const attemptedAtText = data.created_at
    ? new Date(data.created_at).toLocaleString()
    : null;

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold text-center mb-2">
        {data.quiz_title || "Quiz Results"}
      </h2>
      <p className="text-center text-gray-700 mb-6">
        Your Score: <span className="font-semibold">{data.score}</span> /{" "}
        {data.total}
      </p>
      {attemptedAtText && (
        <p className="text-center text-sm text-gray-500 mb-6">
          Attempted on {attemptedAtText}
        </p>
      )}

      <div className="space-y-4">
        {data.results && data.results.length > 0 ? (
          data.results.map((r, idx) => (
            <div
              key={idx}
              className={`border rounded p-4 shadow-sm ${
                r.is_correct ? "bg-green-100" : "bg-red-100"
              }`}
            >
              <h4 className="font-semibold mb-1">
                {idx + 1}. {r.question}
              </h4>
              <p>
                Your answer:{" "}
                {r.user_answer ? (
                  <span className="font-medium">{r.user_answer}</span>
                ) : (
                  <em>(blank)</em>
                )}
              </p>

              {/* ✅ Always show correct answer, especially when wrong */}
              <p>
                Correct answer:{" "}
                <span className="font-semibold">{r.correct_answer}</span>
              </p>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500">
            No question details available.
          </div>
        )}
      </div>

      <div className="text-center mt-8 space-x-3">
        <button
          onClick={() => navigate("/")}
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700"
        >
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Results;
