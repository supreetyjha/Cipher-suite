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

async function get(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

// Classical ciphers
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

// AES
export const generateAESKey = () => get("/symmetric/aes/generate-key");
export const aesEncrypt = (text, key, mode) => post("/symmetric/aes/encrypt", { text, key, mode });
export const aesDecrypt = (ciphertext, key, mode, iv, tag) =>
  post("/symmetric/aes/decrypt", { ciphertext, key, mode, iv, tag });

// ChaCha20
export const generateChaCha20Key = () => get("/symmetric/chacha20/generate-key");
export const chacha20Encrypt = (text, key) => post("/symmetric/chacha20/encrypt", { text, key });
export const chacha20Decrypt = (ciphertext, key, nonce) =>
  post("/symmetric/chacha20/decrypt", { ciphertext, key, nonce });

// RSA
export const generateRSAKeypair = () => get("/asymmetric/rsa/generate-keypair");
export const rsaEncrypt = (text, publicKey) => post("/asymmetric/rsa/encrypt", { text, public_key: publicKey });
export const rsaDecrypt = (ciphertext, privateKey) =>
  post("/asymmetric/rsa/decrypt", { ciphertext, private_key: privateKey });
export const rsaSign = (message, privateKey) => post("/asymmetric/rsa/sign", { message, private_key: privateKey });
export const rsaVerify = (message, signature, publicKey) =>
  post("/asymmetric/rsa/verify", { message, signature, public_key: publicKey });

// Hashing
export const hashPassword = (password) => post("/hashing/password/hash", { password });
export const verifyPassword = (password, hashed) => post("/hashing/password/verify", { password, hashed });
export const computeDigest = (text, algorithm) => post("/hashing/digest", { text, algorithm });
export const deriveKey = (passphrase) => post("/hashing/kdf", { passphrase });