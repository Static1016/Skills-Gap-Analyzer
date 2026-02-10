import { useState } from "react";
import Header from "../components/Header";
import JobSelector from "../components/JobSelector";
import ResultCard from "../components/ResultCard";

const API_BASE = "http://127.0.0.1:8000";

export default function Home() {
  const [category, setCategory] = useState("");
  const [role, setRole] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!category || !role) {
      alert("Please select job category and role.");
      return;
    }

    if (!file) {
      alert("Please upload a resume PDF.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("category", category);
      formData.append("role", role);
      formData.append("resume", file); // MUST be 'resume'

      // jobUrl is optional — only append if backend supports it
      if (jobUrl) {
        formData.append("job_input", jobUrl);
      }

      const response = await fetch(`${API_BASE}/analyze-job`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-6xl mx-auto px-6 py-10 space-y-6">
        {/* Step 1 */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="font-semibold mb-4">
            1. Select Job Category & Role
          </h3>
          <JobSelector
            onSelect={(c, r) => {
              setCategory(c);
              setRole(r);
              setResult(null);
            }}
          />
        </div>

        {/* Step 2 */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="font-semibold mb-4">
            2. Paste Job Opening Link (Optional)
          </h3>
          <input
            type="url"
            placeholder="https://company.com/careers/job-opening"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            className="border p-2 w-full"
          />
        </div>

        {/* Step 3 */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="font-semibold mb-4">
            3. Upload Resume (PDF)
          </h3>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        {/* Button */}
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className={`w-full py-3 rounded text-white font-medium ${
            loading
              ? "bg-gray-400"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Analyzing..." : "Analyze Resume vs Job"}
        </button>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-xl shadow p-6">
            <ResultCard data={result} />
          </div>
        )}
      </main>

      <footer className="mt-16 py-6 text-center text-sm text-gray-500">
        © {new Date().getFullYear()} Skill Gap Analyzer
      </footer>
    </div>
  );
}
