// import React, { useState } from "react";
// import axios from "axios";

// const TextSummarizer = ({ setSummary }) => {
//   const [text, setText] = useState("");

//   const handleSummarize = async () => {
//     if (!text.trim()) return alert("Enter some text first.");
//     try {
//       const res = await axios.post("http://127.0.0.1:5000/summarize-text", { text });
//       setSummary(res.data.summary);
//     } catch (err) {
//       alert(err.response?.data?.error || "Error summarizing text.");
//     }
//   };

//   return (
//     <div className="text-section">
//       <h3>Type Complaint Manually</h3>
//       <textarea
//         placeholder="Type or paste your complaint here..."
//         rows="10"
//         value={text}
//         onChange={(e) => setText(e.target.value)}
//       />
//       <button onClick={handleSummarize}>Summarize Text</button>
//     </div>
//   );
// };

// export default TextSummarizer;
import React, { useState } from "react";
import axios from "axios";

const TextSummarizer = ({ setSummary }) => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!text.trim()) return alert("Enter some text first.");
    try {
      setLoading(true);
      setSummary("");
      const res = await axios.post("http://127.0.0.1:5000/summarize-text", { text });
      setSummary(res.data.summary);
    } catch (err) {
      alert(err.response?.data?.error || "Error summarizing text.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-section">
      <h3>Type Complaint Manually</h3>
      <textarea
        placeholder="Type or paste your complaint here..."
        rows="10"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleSummarize} disabled={loading}>
        {loading ? "Processing..." : "Summarize Text"}
      </button>

      {loading && (
        <div>
          <div className="loader"></div>
          <div className="loading-text">Summarizing complaint...</div>
        </div>
      )}
    </div>
  );
};

export default TextSummarizer;
