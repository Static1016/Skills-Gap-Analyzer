import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer
} from "recharts";

export default function SkillGapChart({ gaps }) {
  const data = gaps.missing.map(skill => ({
    skill,
    gap: 100
  }));

  return (
    <div className="w-full h-[250px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="skill" />
          <YAxis />
          <Bar dataKey="gap" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
