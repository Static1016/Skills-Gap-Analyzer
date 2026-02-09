import { useState } from "react";
import ResumeUpload from "../components/ResumeUpload";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">
          Skill Gap Analyzer
        </h1>

        <ResumeUpload onResult={setResult} />

        {result && <ResultCard data={result} />}
      </div>
    </div>
  );
}
