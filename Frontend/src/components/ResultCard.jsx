export default function ResultCard({ data }) {
  return (
    <div className="mt-8 bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">
        Job Fit Score: {data.job_fit_score}%
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-medium text-red-600 mb-2">Missing Skills</h3>
          <ul className="list-disc ml-6">
            {data.gaps.missing.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-medium text-yellow-600 mb-2">Needs Improvement</h3>
          <ul className="list-disc ml-6">
            {data.gaps.weak.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
