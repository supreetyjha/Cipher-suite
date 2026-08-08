import { useState } from "react";
import { generateAESKey, aesEncrypt } from "../api/client";

function bytesToColor(bytes, offset) {
  const r = bytes[offset] || 0;
  const g = bytes[offset + 1] || 0;
  const b = bytes[offset + 2] || 0;
  return `rgb(${r}, ${g}, ${b})`;
}

function base64ToBytes(b64) {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

function BlockGrid({ label, ciphertextB64 }) {
  const bytes = base64ToBytes(ciphertextB64);
  const blockCount = Math.floor(bytes.length / 16);
  const blocks = Array.from({ length: blockCount }, (_, i) => bytesToColor(bytes, i * 16));

  return (
    <div className="mb-4">
      <label className="block text-xs text-neutral-500 mb-2">{label}</label>
      <div className="flex gap-1 flex-wrap">
        {blocks.map((color, i) => (
          <div
            key={i}
            style={{ backgroundColor: color }}
            className="w-10 h-10 rounded border border-neutral-800"
            title={`Block ${i}`}
          />
        ))}
      </div>
    </div>
  );
}

function ECBVisualizer() {
  const [ecbResult, setEcbResult] = useState(null);
  const [cbcResult, setCbcResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runDemo() {
    setError("");
    setLoading(true);
    try {
      const key = (await generateAESKey()).key;
      // Repeat a 16-byte block 6 times — identical plaintext blocks throughout
      const plaintext = "PATTERN_BLOCK_16".repeat(6).slice(0, 96);

      const ecb = await aesEncrypt(plaintext, key, "ECB");
      const cbc = await aesEncrypt(plaintext, key, "CBC");

      setEcbResult(ecb.ciphertext);
      setCbcResult(cbc.ciphertext);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <p className="text-xs text-neutral-500 mb-4">
        Encrypts the same 16-byte plaintext block, repeated 6 times, using the same AES key
        under both ECB and CBC mode. Each square represents one encrypted block's first 3 bytes,
        rendered as a color.
      </p>

      <button
        onClick={runDemo}
        disabled={loading}
        className="w-full bg-neutral-100 text-neutral-900 text-sm rounded px-3 py-2 mb-4 disabled:opacity-40"
      >
        {loading ? "Encrypting..." : "Run ECB vs CBC Comparison"}
      </button>

      {error && <p className="text-xs text-red-400 mb-2">{error}</p>}

      {ecbResult && (
        <>
          <BlockGrid label="ECB Mode — identical plaintext blocks → identical colors (pattern leaks)" ciphertextB64={ecbResult} />
          <BlockGrid label="CBC Mode — identical plaintext blocks → different colors (no pattern)" ciphertextB64={cbcResult} />
          <p className="text-xs text-neutral-600 mt-2">
            This is why ECB is considered insecure for anything beyond a single block: repeating
            plaintext structure (like image pixels or padded records) remains visible in the ciphertext.
            CBC's chaining (each block XORed with the previous ciphertext block) eliminates this leak.
          </p>
        </>
      )}
    </div>
  );
}

export default ECBVisualizer;