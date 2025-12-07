import React, { useEffect, useState } from "react";
import { getMyResults } from "../services/api";
import { useNavigate } from "react-router-dom";

function MyResults() {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getMyResults()
      .then((res) => setResults(res.data))
      .catch((err) => console.error("Error loading results:", err));
  }, []);

  if (!results.length)
    return <div className="p-6 text-center text-gray-600">No results yet.</div>;

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-center">My Quiz Results</h2>
      <div className="space-y-4">
        {results.map((r) => (
          <div
            key={r.id}
            className="border rounded-lg p-4 shadow-sm bg-gray-50 text-center"
          >
            <p className="text-xl font-semibold">{r.quiz_title}</p>
            <p className="mt-1 text-gray-700">
              Score: <span className="font-medium">{r.score}</span> / {r.total}
            </p>
            {r.created_at && (
              <p className="text-sm text-gray-500 mt-1">
                Taken on {new Date(r.created_at).toLocaleString()}
              </p>
            )}
            <button
              className="mt-3 bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
              onClick={() => navigate(`/results/${r.id}`)}
            >
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MyResults;
