import React, { useState } from "react";
import Tabs from "../components/Tabs";
import LegalIssue from "../components/LegalIssue";
import ActExplanation from "../components/ActExplanation";
import VoiceHelp from "../components/Voicehelp";

function Assistant() {
  const [activeTab, setActiveTab] = useState("issue");

  const renderTab = () => {
    if (activeTab === "issue") return <LegalIssue />;
    if (activeTab === "act") return <ActExplanation />;
    if (activeTab === "voice") return <VoiceHelp />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-primary-50/20 to-indigo-50/30">
      <div className="max-w-4xl mx-auto px-4 py-8 md:py-12">
        <div className="text-center mb-8">
          <h1 className="text-2xl md:text-3xl font-bold text-slate-800">Legal Assistant</h1>
          <p className="text-slate-600 mt-1">Choose how you&apos;d like to get legal guidance</p>
        </div>
        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
        <div className="content mt-6">{renderTab()}</div>
      </div>
    </div>
  );
}

export default Assistant;
