import React from "react";

function QuestionCard({ question, index, onAnswer }) {
  return (
    <div className="border rounded p-4 shadow-sm bg-gray-50">
      <p className="font-semibold mb-2">
        {index + 1}. {question.text}
      </p>
      <input
        type="text"
        className="w-full border px-3 py-2 rounded"
        placeholder="Your answer..."
        onChange={(e) => onAnswer(index, e.target.value)}
      />
    </div>
  );
}

export default QuestionCard;
