import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import TextSummarizer from "./components/TextSummarizer";
import SummaryDisplay from "./components/SummaryDisplay";
import "./App.css";

function App() {
  const [summary, setSummary] = useState("");

  return (
    <div className="app-container">
      <h1>Complaint Summarizer</h1>
      <div className="input-section">
        <FileUpload setSummary={setSummary} />
        <TextSummarizer setSummary={setSummary} />
      </div>
      <SummaryDisplay summary={summary} />
    </div>
  );
}

export default App;
