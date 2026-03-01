import React, { useState } from "react";

function LegalIssue() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askBackend = async () => {
    if (!question.trim()) {
      alert("Please enter your issue first");
      return;
    }

    setLoading(true);
    setAnswer(null);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error("Backend error");
      }

      const data = await res.json();

      setAnswer(data);

    } catch (err) {
      console.error(err);
      setError("Server error. Please check if backend is running.");
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Describe your legal issue</h2>

      <textarea
        placeholder="E.g., My parents are forcing me to marry."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        className="primary-btn"
        onClick={askBackend}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Ask"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {answer && (
        <div className="response">
          <h3>Legal Guidance</h3>

          {answer.law && (
            <>
              <h4>Law</h4>
              <p>{answer.law}</p>
            </>
          )}

          {answer.meaning && (
            <>
              <h4>Meaning</h4>
              <p>{answer.meaning}</p>
            </>
          )}

          {answer.steps && (
            <>
              <h4>What You Can Do</h4>
              <ul>
                {answer.steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ul>
            </>
          )}

          {answer.answer && (
            <p style={{ whiteSpace: "pre-line" }}>
              {answer.answer}
            </p>
          )}

          <p className="disclaimer">
            Disclaimer: This is general guidance. Please consult a lawyer for
            professional legal advice.
          </p>
        </div>
      )}
    </div>
  );
}

export default LegalIssue;