import { useEffect, useState } from "react";
import { getJobRoles } from "../api/analyzer";

export default function JobSelector({ onSelect }) {
  const [roles, setRoles] = useState({});
  const [category, setCategory] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    getJobRoles().then(setRoles);
  }, []);

  useEffect(() => {
    if (category && role) {
      onSelect(category, role);
    }
  }, [category, role]);

  return (
    <div className="bg-white p-6 rounded shadow mb-6">
      <select
        className="border p-2 w-full mb-4"
        onChange={(e) => {
          setCategory(e.target.value);
          setRole("");
        }}
      >
        <option value="">Select Job Category</option>
        {Object.keys(roles).map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      {category && (
        <select
          className="border p-2 w-full"
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="">Select Job Role</option>
          {Object.entries(roles[category]).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      )}
    </div>
  );
}
