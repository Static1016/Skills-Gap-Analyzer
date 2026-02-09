import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function SkillGapChart({ gaps }) {
  if (!gaps) return null;

  const chartData = [
    ...(gaps.missing || []).map(skill => ({
      skill,
      value: 1
    })),
    ...(gaps.weak || []).map(skill => ({
      skill,
      value: 0.5
    }))
  ];

  if (chartData.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        No skill gaps to display.
      </p>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={chartData}>
        <XAxis dataKey="skill" />
        <YAxis hide />
        <Tooltip />
        <Bar
          dataKey="value"
          fill="#ef4444"
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
