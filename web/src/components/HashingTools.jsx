import { useState } from "react";
import { hashPassword, verifyPassword, computeDigest, deriveKey } from "../api/client";

function HashingTools() {
  const [tool, setTool] = useState("password");
  const [password, setPassword] = useState("");
  const [hashed, setHashed] = useState("");
  const [text, setText] = useState("");
  const [algorithm, setAlgorithm] = useState("sha256");
  const [passphrase, setPassphrase] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRun() {
    setError("");
    setResult("");
    setLoading(true);
    try {
      if (tool === "password") {
        const data = await hashPassword(password);
        setHashed(data.hashed);
        setResult(data.hashed);
      } else if (tool === "verify") {
        const data = await verifyPassword(password, hashed);
        setResult(data.valid ? "✓ Password matches" : "✗ Password does not match");
      } else if (tool === "digest") {
        const data = await computeDigest(text, algorithm);
        setResult(data.hash);
      } else if (tool === "kdf") {
        const data = await deriveKey(passphrase);
        setResult(JSON.stringify(data, null, 2));
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <label className="block text-xs text-neutral-500 mb-1">Tool</label>
      <select
        value={tool}
        onChange={(e) => { setTool(e.target.value); setResult(""); setError(""); }}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
      >
        <option value="password">Hash Password (Argon2)</option>
        <option value="verify">Verify Password</option>
        <option value="digest">SHA Digest</option>
        <option value="kdf">Key Derivation (Argon2 KDF)</option>
      </select>

      {(tool === "password" || tool === "verify") && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Password</label>
          <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          />
        </>
      )}

      {tool === "verify" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Stored Hash</label>
          <textarea
            value={hashed}
            onChange={(e) => setHashed(e.target.value)}
            rows={2}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-3 font-mono"
          />
        </>
      )}

      {tool === "digest" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Text</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={2}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          />
          <label className="block text-xs text-neutral-500 mb-1">Algorithm</label>
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          >
            <option value="sha256">SHA-256</option>
            <option value="sha512">SHA-512</option>
          </select>
        </>
      )}

      {tool === "kdf" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Passphrase</label>
          <input
            value={passphrase}
            onChange={(e) => setPassphrase(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          />
        </>
      )}

      <button
        onClick={handleRun}
        disabled={loading}
        className="w-full bg-neutral-100 text-neutral-900 text-sm rounded px-3 py-2 mb-3 disabled:opacity-40"
      >
        Run
      </button>

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

export default HashingTools;