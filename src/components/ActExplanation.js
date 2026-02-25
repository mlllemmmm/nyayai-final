import React, { useState } from "react";

function ActExplanation() {
  const [actName, setActName] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExplain = async () => {
    if (!actName) return;

    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/explain-act", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ act_name: actName }),
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error("Error:", error);
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Understand an Act</h2>

      <input
        type="text"
        placeholder="Enter Act name (e.g., consumer_protection_act)"
        value={actName}
        onChange={(e) => setActName(e.target.value)}
      />

      <button className="primary-btn" onClick={handleExplain}>
        Explain
      </button>

      {loading && <p>Generating explanation...</p>}

      {response && response.explanation && (
        <div className="response">
          <h3>{response.act}</h3>
          <p>{response.explanation}</p>
        </div>
      )}

      {response && response.answer && (
        <div className="response">
          <p>{response.answer}</p>
        </div>
      )}
    </div>
  );
}

export default ActExplanation;