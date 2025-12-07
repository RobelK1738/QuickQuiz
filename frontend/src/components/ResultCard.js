import React from "react";

function ResultCard({ result }) {
  return (
    <div
      className={`border p-4 rounded shadow-sm ${
        result.correct ? "bg-green-100" : "bg-red-100"
      }`}
    >
      <h4 className="font-semibold mb-1">{result.question}</h4>
      <p>Your answer: {result.user_answer}</p>
      <p>Correct answer: {result.correct_answer}</p>
    </div>
  );
}

export default ResultCard;
