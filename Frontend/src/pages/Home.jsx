import { useState } from "react";
import JobSelector from "../components/JobSelector";
import ResumeUpload from "../components/ResumeUpload";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [category, setCategory] = useState("");
  const [role, setRole] = useState("");
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 px-6 py-10">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <h1 className="text-3xl font-bold text-center mb-8">
          Skill Gap Analyzer
        </h1>

        {/* Job Selection */}
        <JobSelector
          onSelect={(selectedCategory, selectedRole) => {
            setCategory(selectedCategory);
            setRole(selectedRole);
            setResult(null); // reset previous result
          }}
        />

        {/* Resume Upload */}
        <ResumeUpload
          category={category}
          role={role}
          onResult={setResult}
        />

        {/* Results */}
        {result && <ResultCard data={result} />}
      </div>
    </div>
  );
}
