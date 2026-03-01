import React from "react";

function Tabs({ activeTab, setActiveTab }) {
  const base = "px-4 py-2.5 rounded-full text-sm font-medium transition-all border";
  const inactive = "border-slate-200 bg-white text-slate-600 hover:bg-slate-50";
  const active = "border-transparent bg-primary-800 text-white shadow-md";

  return (
    <div className="flex flex-wrap justify-center gap-2">
      <button
        className={activeTab === "issue" ? `${base} ${active}` : `${base} ${inactive}`}
        onClick={() => setActiveTab("issue")}
      >
        Facing a Legal Issue
      </button>
      <button
        className={activeTab === "act" ? `${base} ${active}` : `${base} ${inactive}`}
        onClick={() => setActiveTab("act")}
      >
        Understand an Act
      </button>
      <button
        className={activeTab === "voice" ? `${base} ${active}` : `${base} ${inactive}`}
        onClick={() => setActiveTab("voice")}
      >
        Voice Legal Help
      </button>
    </div>
  );
}

export default Tabs;
