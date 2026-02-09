import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function ResumeUpload({ category, role, onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!category || !role) {
      alert("Please select a job category and role first.");
      return;
    }

    if (!file) {
      alert("Please upload a PDF resume.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_BASE}/analyze-resume?category=${category}&role=${role}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();
      onResult(data);
    } catch (err) {
      alert("Resume analysis failed. Check backend.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow mb-6">
      <label className="block mb-2 font-medium">
        Upload Resume (PDF only)
      </label>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 block w-full"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`w-full px-4 py-2 rounded text-white transition ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}
