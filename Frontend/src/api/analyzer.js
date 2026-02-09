const API_BASE = "http://127.0.0.1:8000";

export async function analyzeResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/analyze-resume`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("API Error");
  }

  return res.json();
}
