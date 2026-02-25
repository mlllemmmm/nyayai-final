import React, { useState } from "react";
import Header from "./components/Header";
import Tabs from "./components/Tabs";
import LegalIssue from "./components/LegalIssue";
import ActExplanation from "./components/ActExplanation";
import VoiceHelp from "./components/Voicehelp";

function App() {
  const [activeTab, setActiveTab] = useState("issue");

  const renderTab = () => {
    if (activeTab === "issue") return <LegalIssue />;
    if (activeTab === "act") return <ActExplanation />;
    if (activeTab === "voice") return <VoiceHelp />;
  };

  return (
    <div className="app">
      <Header />
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="content">{renderTab()}</div>
    </div>
  );
}

export default App;
