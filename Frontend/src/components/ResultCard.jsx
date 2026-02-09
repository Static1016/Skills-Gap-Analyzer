import SkillGapChart from "./SkillGapChart";
import FitDonut from "./FitDonut";

export default function ResultCard({ data }) {
  // Normalize data
  const fit = Math.round(data.job_fit_score || 0);

  const gaps = data.gaps || {
    missing: data.missing_skills || [],
    weak: [],
    strong: []
  };

  const roleName = data.role || "Job Posting";

  return (
    <div className="space-y-10">
      {/* Fit Score + Chart */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Fit Score */}
        <div>
          <h4 className="font-semibold mb-3">
            Job Fit Overview
          </h4>

          {/* Give donut a stable container */}
          <div className="h-64 flex items-center justify-center">
            <FitDonut score={fit} />
          </div>

          <p className="text-sm text-gray-600 text-center mt-2">
            Match for {roleName}
          </p>
        </div>

        {/* Skill Gap Chart */}
        <div>
          <h4 className="font-semibold mb-3">
            Skill Gap Distribution
          </h4>

          {/* 🔑 FIX: explicit height wrapper */}
          <div className="h-64 w-full">
            <SkillGapChart gaps={gaps} />
          </div>
        </div>
      </div>

      {/* Skill Lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-red-600 mb-2">
            Missing Skills
          </h4>

          {gaps.missing.length === 0 ? (
            <p className="text-sm text-gray-500">None 🎉</p>
          ) : (
            <ul className="list-disc ml-5">
              {gaps.missing.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h4 className="font-semibold text-yellow-600 mb-2">
            Needs Improvement
          </h4>

          {gaps.weak.length === 0 ? (
            <p className="text-sm text-gray-500">Looks good</p>
          ) : (
            <ul className="list-disc ml-5">
              {gaps.weak.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h4 className="font-semibold mb-3">
          Recommended Learning Path
        </h4>

        {!data.recommendations || data.recommendations.length === 0 ? (
          <p className="text-sm text-gray-500">
            No learning resources available.
          </p>
        ) : (
          data.recommendations.map((r) => (
            <div
              key={r.skill}
              className="border rounded-lg p-4 mb-3"
            >
              <p className="font-medium mb-1">{r.skill}</p>
              <ul className="list-disc ml-5 text-sm">
                {r.resources.map((res, idx) => (
                  <li key={idx}>
                    <a
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      ▶️ {res.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
