const BASE_URL = "http://127.0.0.1:8000";

export async function encryptCaesar(text, shift) {
  const res = await fetch(`${BASE_URL}/classical/caesar/encrypt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, shift }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export async function decryptCaesar(text, shift) {
  const res = await fetch(`${BASE_URL}/classical/caesar/decrypt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, shift }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}