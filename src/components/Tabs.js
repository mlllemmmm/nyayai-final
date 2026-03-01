import React from "react";

function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs">
      <button
        className={activeTab === "issue" ? "active" : ""}
        onClick={() => setActiveTab("issue")}
      >
        Facing a Legal Issue
      </button>

      <button
        className={activeTab === "act" ? "active" : ""}
        onClick={() => setActiveTab("act")}
      >
        Understand an Act
      </button>

      <button
        className={activeTab === "voice" ? "active" : ""}
        onClick={() => setActiveTab("voice")}
      >
        Voice Legal Help
      </button>
    </div>
  );
}

export default Tabs;
