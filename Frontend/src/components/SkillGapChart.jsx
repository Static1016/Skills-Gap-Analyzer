import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function SkillGapChart({ gaps }) {
  const data = gaps.missing.map((skill) => ({
    skill,
    value: 100
  }));

  if (data.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        No missing skills 🎉
      </p>
    );
  }

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="skill" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Bar dataKey="value" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
