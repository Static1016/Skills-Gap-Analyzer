import { useState } from "react";
import { analyzeResume } from "../api/analyzer";

export default function ResumeUpload({ onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please upload a PDF resume");
      return;
    }

    setLoading(true);
    try {
      const data = await analyzeResume(file);
      onResult(data);
    } catch (err) {
      alert("Analysis failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 block"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`w-full px-4 py-2 rounded text-white ${
          loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}
