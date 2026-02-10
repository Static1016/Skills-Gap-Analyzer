import SkillGapChart from "./SkillGapChart";
import FitDonut from "./FitDonut";

export default function ResultCard({ data }) {
  if (!data) return null;

  return (
    <div className="space-y-10">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-semibold mb-3">Job Fit Overview</h4>
          <FitDonut score={data.job_fit_score} />
        </div>

        <div>
          <h4 className="font-semibold mb-3">Skill Gap Distribution</h4>
          <SkillGapChart gaps={data.gaps} />
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-red-600 font-semibold">Missing Skills</h4>
          <ul className="list-disc ml-5">
            {data.gaps.missing.map(s => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-yellow-600 font-semibold">Needs Improvement</h4>
          <ul className="list-disc ml-5">
            {data.gaps.weak.map(s => (
              <li key={s}>{s}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
