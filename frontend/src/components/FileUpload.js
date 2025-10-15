// import React, { useState } from "react";
// import axios from "axios";

// const FileUpload = ({ setSummary }) => {
//   const [file, setFile] = useState(null);

//   const handleUpload = async () => {
//     if (!file) return alert("Please select a file first.");
//     const formData = new FormData();
//     formData.append("file", file);

//     try {
//       const res = await axios.post("http://127.0.0.1:5000/ocr-summarize", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });
//       setSummary(res.data.summary);
//     } catch (err) {
//       alert(err.response?.data?.error || "Error processing file.");
//     }
//   };

//   return (
//     <div className="upload-section">
//       <h3>Upload Handwritten Complaint</h3>
//       <input type="file" accept="image/*,.pdf" onChange={(e) => setFile(e.target.files[0])} />
//       <button onClick={handleUpload}>Summarize Image</button>
//     </div>
//   );
// };

// export default FileUpload;

import React, { useState } from "react";
import axios from "axios";

const FileUpload = ({ setSummary }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");
    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setSummary("");
      const res = await axios.post("http://127.0.0.1:5000/ocr-summarize", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSummary(res.data.summary);
    } catch (err) {
      alert(err.response?.data?.error || "Error processing file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <h3>Upload Handwritten Complaint</h3>
      <input type="file" accept="image/*,.pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Summarize Image"}
      </button>

      {loading && (
        <div>
          <div className="loader"></div>
          <div className="loading-text">Extracting and summarizing your complaint...</div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
