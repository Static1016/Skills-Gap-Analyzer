import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from "recharts";

export default function SkillGapChart({ gaps }) {
  if (!gaps) return null;

  const data = [
    ...gaps.missing.map((s) => ({
      skill: s,
      value: 100,
      type: "missing"
    })),
    ...gaps.weak.map((s) => ({
      skill: s,
      value: 50,
      type: "weak"
    }))
  ];

  if (data.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        No skill gaps detected 🎉
      </p>
    );
  }

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="skill" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Bar dataKey="value">
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={
                  entry.type === "missing"
                    ? "#ef4444"   // red
                    : "#facc15"   // yellow
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
