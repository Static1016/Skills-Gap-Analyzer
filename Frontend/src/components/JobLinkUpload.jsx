import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function JobLinkUpload({ onResult }) {
  const [file, setFile] = useState(null);
  const [jobUrl, setJobUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!jobUrl) {
      alert("Please paste a job posting URL.");
      return;
    }

    if (!file) {
      alert("Please upload a resume PDF.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_BASE}/analyze-job-link?job_url=${encodeURIComponent(jobUrl)}`,
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
      console.error(err);
      alert("Job link analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="block mb-2 font-medium">
        Job Posting URL
      </label>
      <input
        type="url"
        placeholder="https://company.com/careers/job-posting"
        value={jobUrl}
        onChange={(e) => setJobUrl(e.target.value)}
        className="border p-2 w-full mb-4"
      />

      <label className="block mb-2 font-medium">
        Upload Resume (PDF)
      </label>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`w-full px-4 py-2 rounded text-white ${
          loading
            ? "bg-gray-400"
            : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Job Match"}
      </button>
    </div>
  );
}
