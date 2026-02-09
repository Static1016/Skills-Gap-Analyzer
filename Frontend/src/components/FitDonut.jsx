import { PieChart, Pie, Cell } from "recharts";

export default function FitDonut({ score }) {
  const data = [
    { name: "Fit", value: score },
    { name: "Gap", value: 100 - score }
  ];

  const COLORS = ["#22c55e", "#e5e7eb"];

  return (
    <div className="relative flex items-center justify-center">
      <PieChart width={200} height={200}>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          dataKey="value"
          startAngle={90}
          endAngle={-270}
        >
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={COLORS[index]} />
          ))}
        </Pie>
      </PieChart>

      {/* Center text */}
      <div className="absolute text-center pointer-events-none">
        <p className="text-2xl font-bold">{score}%</p>
        <p className="text-xs text-gray-500">Fit Score</p>
      </div>
    </div>
  );
}
