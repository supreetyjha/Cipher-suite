import { useState } from "react";
import {
  generateAESKey, aesEncrypt, aesDecrypt,
  generateChaCha20Key, chacha20Encrypt, chacha20Decrypt,
} from "../api/client";

const AES_MODES = ["ECB", "CBC", "CFB", "OFB", "GCM"];

function ModernCrypto() {
  const [algo, setAlgo] = useState("aes");
  const [mode, setMode] = useState("GCM");
  const [key, setKey] = useState("");
  const [text, setText] = useState("");
  const [ciphertext, setCiphertext] = useState("");
  const [iv, setIv] = useState("");
  const [tag, setTag] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGenerateKey() {
    setError("");
    try {
      const data = algo === "aes" ? await generateAESKey() : await generateChaCha20Key();
      setKey(data.key);
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleEncrypt() {
    setError("");
    setResult("");
    setLoading(true);
    try {
      if (algo === "aes") {
        const data = await aesEncrypt(text, key, mode);
        setCiphertext(data.ciphertext);
        setIv(data.iv || "");
        setTag(data.tag || "");
        setResult(JSON.stringify(data, null, 2));
      } else {
        const data = await chacha20Encrypt(text, key);
        setCiphertext(data.ciphertext);
        setIv(data.nonce);
        setResult(JSON.stringify(data, null, 2));
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDecrypt() {
    setError("");
    setResult("");
    setLoading(true);
    try {
      if (algo === "aes") {
        const data = await aesDecrypt(ciphertext, key, mode, iv || null, tag || null);
        setResult(data.plaintext);
      } else {
        const data = await chacha20Decrypt(ciphertext, key, iv);
        setResult(data.plaintext);
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <label className="block text-xs text-neutral-500 mb-1">Algorithm</label>
      <select
        value={algo}
        onChange={(e) => { setAlgo(e.target.value); setResult(""); setError(""); }}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
      >
        <option value="aes">AES-256</option>
        <option value="chacha20">ChaCha20</option>
      </select>

      {algo === "aes" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Mode</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          >
            {AES_MODES.map((m) => <option key={m} value={m}>{m}</option>)}
          </select>
        </>
      )}

      <label className="block text-xs text-neutral-500 mb-1">Key (base64)</label>
      <div className="flex gap-2 mb-3">
        <input
          value={key}
          onChange={(e) => setKey(e.target.value)}
          className="flex-1 bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs"
          placeholder="Click generate, or paste your own"
        />
        <button
          onClick={handleGenerateKey}
          className="border border-neutral-700 text-xs rounded px-3 py-2 whitespace-nowrap"
        >
          Generate Key
        </button>
      </div>

      <label className="block text-xs text-neutral-500 mb-1">Plaintext (for encrypt)</label>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={2}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
      />

      <div className="flex gap-2 mb-3">
        <button
          onClick={handleEncrypt}
          disabled={loading || !text || !key}
          className="flex-1 bg-neutral-100 text-neutral-900 text-sm rounded px-3 py-2 disabled:opacity-40"
        >
          Encrypt
        </button>
        <button
          onClick={handleDecrypt}
          disabled={loading || !ciphertext || !key}
          className="flex-1 border border-neutral-700 text-sm rounded px-3 py-2 disabled:opacity-40"
        >
          Decrypt
        </button>
      </div>

      <label className="block text-xs text-neutral-500 mb-1">Ciphertext (for decrypt)</label>
      <input
        value={ciphertext}
        onChange={(e) => setCiphertext(e.target.value)}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-2"
      />
      <div className="grid grid-cols-2 gap-2 mb-3">
        <input
          value={iv}
          onChange={(e) => setIv(e.target.value)}
          placeholder={algo === "aes" ? "IV" : "Nonce"}
          className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs"
        />
        {algo === "aes" && mode === "GCM" && (
          <input
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="Tag"
            className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs"
          />
        )}
      </div>

      {error && <p className="text-xs text-red-400 mb-2">{error}</p>}

      {result && (
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Result</label>
          <pre className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs whitespace-pre-wrap break-all">
            {result}
          </pre>
        </div>
      )}
    </div>
  );
}

export default ModernCrypto;