import SkillGapChart from "./SkillGapChart";
import FitDonut from "./FitDonut";

export default function ResultCard({ data }) {
  if (!data) return null;

  const { job_fit_score, gaps, recommendations, role } = data;

  return (
    <div className="space-y-10">
      {/* Top charts */}
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-semibold mb-3">Job Fit Overview</h4>
          <FitDonut score={job_fit_score} />
          {role && (
            <p className="text-sm text-gray-500 text-center mt-2">
              Match for {role}
            </p>
          )}
        </div>

        <div>
          <h4 className="font-semibold mb-3">Skill Gap Distribution</h4>
          <SkillGapChart gaps={gaps} />
        </div>
      </div>

      {/* Skill lists */}
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-red-600 font-semibold mb-2">
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
          <h4 className="text-yellow-600 font-semibold mb-2">
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

        {!recommendations || recommendations.length === 0 ? (
          <p className="text-sm text-gray-500">
            No learning resources available.
          </p>
        ) : (
          recommendations.map((rec) => (
            <div
              key={rec.skill}
              className="border rounded-lg p-4 mb-3"
            >
              <p className="font-medium mb-1">
                {rec.skill}
              </p>
              <ul className="list-disc ml-5 text-sm">
                {rec.resources.map((res, idx) => (
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
