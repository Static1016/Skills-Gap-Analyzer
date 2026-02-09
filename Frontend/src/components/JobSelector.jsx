import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function JobSelector({ onSelect }) {
  const [rolesData, setRolesData] = useState({});
  const [category, setCategory] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/job-roles`)
      .then((res) => res.json())
      .then((data) => setRolesData(data))
      .catch((err) => console.error("Failed to load roles", err));
  }, []);

  const categories = Object.keys(rolesData);
  const roles =
    category && rolesData[category]
      ? Object.keys(rolesData[category])
      : [];

  const handleCategoryChange = (e) => {
    const selected = e.target.value;
    setCategory(selected);
    setRole("");
    onSelect(selected, "");
  };

  const handleRoleChange = (e) => {
    const selected = e.target.value;
    setRole(selected);
    onSelect(category, selected);
  };

  return (
    <div className="space-y-4">
      {/* Category Dropdown */}
      <select
        value={category}
        onChange={handleCategoryChange}
        className="border p-2 w-full"
      >
        <option value="">Select category</option>
        {categories.map((cat) => (
          <option key={cat} value={cat}>
            {cat.toUpperCase()}
          </option>
        ))}
      </select>

      {/* Role Dropdown */}
      <select
        value={role}
        onChange={handleRoleChange}
        className="border p-2 w-full"
        disabled={!category}
      >
        <option value="">Select role</option>
        {roles.map((r) => (
          <option key={r} value={r}>
            {r.replace(/_/g, " ").toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}
