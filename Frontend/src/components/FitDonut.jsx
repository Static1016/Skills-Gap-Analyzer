import { PieChart, Pie, Cell } from "recharts";

export default function FitDonut({ score }) {
  const data = [
    { name: "Fit", value: score },
    { name: "Gap", value: 100 - score }
  ];

  const COLORS = ["#22c55e", "#e5e7eb"];

  return (
    <div className="relative flex justify-center items-center h-[220px]">
      <PieChart width={200} height={200}>
        <Pie
          data={data}
          cx={100}
          cy={100}
          innerRadius={60}
          outerRadius={80}
          dataKey="value"
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i]} />
          ))}
        </Pie>
      </PieChart>

      <div className="absolute text-center">
        <p className="text-2xl font-bold">{score}%</p>
        <p className="text-xs text-gray-500">Fit Score</p>
      </div>
    </div>
  );
}
