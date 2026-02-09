export default function ResultCard({ data }) {
  const fit = Math.round(data.job_fit_score);

  return (
    <div className="mt-8 bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-2">
        Job Fit Score
      </h2>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
        <div
          className="h-4 rounded-full bg-green-500"
          style={{ width: `${fit}%` }}
        />
      </div>

      <p className="text-sm text-gray-600 mb-6">
        {fit}% match with ML Engineer role
      </p>

      {/* Skill Gaps */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-semibold text-red-600 mb-2">
            Missing Skills
          </h3>
          {data.gaps.missing.length === 0 ? (
            <p className="text-sm text-gray-500">None 🎉</p>
          ) : (
            <ul className="list-disc ml-6">
              {data.gaps.missing.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h3 className="font-semibold text-yellow-600 mb-2">
            Needs Improvement
          </h3>
          {data.gaps.weak.length === 0 ? (
            <p className="text-sm text-gray-500">Looks good</p>
          ) : (
            <ul className="list-disc ml-6">
              {data.gaps.weak.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div className="mt-8">
        <h3 className="font-semibold mb-3">
          Recommended Learning Path
        </h3>

        {data.recommendations.length === 0 ? (
          <p className="text-sm text-gray-500">
            No recommendations needed.
          </p>
        ) : (
          data.recommendations.map((r) => (
            <div
              key={r.skill}
              className="border rounded p-3 mb-3"
            >
              <p className="font-medium">{r.skill}</p>
              <ul className="list-disc ml-6 text-sm">
                {r.resources.map((res) => (
                  <li key={res}>{res}</li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
