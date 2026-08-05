const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function post(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const caesarEncrypt = (text, shift) => post("/classical/caesar/encrypt", { text, shift });
export const caesarDecrypt = (text, shift) => post("/classical/caesar/decrypt", { text, shift });

export const vigenereEncrypt = (text, key) => post("/classical/vigenere/encrypt", { text, key });
export const vigenereDecrypt = (text, key) => post("/classical/vigenere/decrypt", { text, key });

export const playfairEncrypt = (text, key) => post("/classical/playfair/encrypt", { text, key });
export const playfairDecrypt = (text, key) => post("/classical/playfair/decrypt", { text, key });

export const railFenceEncrypt = (text, rails) => post("/classical/railfence/encrypt", { text, rails });
export const railFenceDecrypt = (text, rails) => post("/classical/railfence/decrypt", { text, rails });

export const analyzeFrequency = (text) => post("/analysis/frequency", { text });
export const bruteForceCaesar = (text) => post("/analysis/bruteforce/caesar", { text });