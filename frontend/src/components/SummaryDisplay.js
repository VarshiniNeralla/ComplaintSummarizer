import React from "react";

const SummaryDisplay = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="summary-section">
      <h3>Summarized Complaint</h3>
      <p>{summary}</p>
    </div>
  );
};

export default SummaryDisplay;
