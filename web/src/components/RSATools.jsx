import { useState } from "react";
import { generateRSAKeypair, rsaEncrypt, rsaDecrypt, rsaSign, rsaVerify } from "../api/client";

function RSATools() {
  const [action, setAction] = useState("encrypt");
  const [publicKey, setPublicKey] = useState("");
  const [privateKey, setPrivateKey] = useState("");
  const [text, setText] = useState("");
  const [ciphertext, setCiphertext] = useState("");
  const [signature, setSignature] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGenerateKeypair() {
    setError("");
    setLoading(true);
    try {
      const data = await generateRSAKeypair();
      setPublicKey(data.public_key);
      setPrivateKey(data.private_key);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleRun() {
    setError("");
    setResult("");
    setLoading(true);
    try {
      if (action === "encrypt") {
        const data = await rsaEncrypt(text, publicKey);
        setCiphertext(data.ciphertext);
        setResult(data.ciphertext);
      } else if (action === "decrypt") {
        const data = await rsaDecrypt(ciphertext, privateKey);
        setResult(data.plaintext);
      } else if (action === "sign") {
        const data = await rsaSign(text, privateKey);
        setSignature(data.signature);
        setResult(data.signature);
      } else if (action === "verify") {
        const data = await rsaVerify(text, signature, publicKey);
        setResult(data.valid ? "✓ Signature valid" : "✗ Signature invalid");
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        onClick={handleGenerateKeypair}
        disabled={loading}
        className="w-full border border-neutral-700 text-xs rounded px-3 py-2 mb-3 disabled:opacity-40"
      >
        Generate RSA-2048 Keypair
      </button>

      <label className="block text-xs text-neutral-500 mb-1">Public Key</label>
      <textarea
        value={publicKey}
        onChange={(e) => setPublicKey(e.target.value)}
        rows={2}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-2 font-mono"
      />
      <label className="block text-xs text-neutral-500 mb-1">Private Key</label>
      <textarea
        value={privateKey}
        onChange={(e) => setPrivateKey(e.target.value)}
        rows={2}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-3 font-mono"
      />

      <label className="block text-xs text-neutral-500 mb-1">Action</label>
      <select
        value={action}
        onChange={(e) => { setAction(e.target.value); setResult(""); setError(""); }}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
      >
        <option value="encrypt">Encrypt (with public key)</option>
        <option value="decrypt">Decrypt (with private key)</option>
        <option value="sign">Sign (with private key)</option>
        <option value="verify">Verify signature (with public key)</option>
      </select>

      {(action === "encrypt" || action === "sign" || action === "verify") && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Message</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={2}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-3"
          />
        </>
      )}

      {action === "decrypt" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Ciphertext</label>
          <input
            value={ciphertext}
            onChange={(e) => setCiphertext(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-3"
          />
        </>
      )}

      {action === "verify" && (
        <>
          <label className="block text-xs text-neutral-500 mb-1">Signature</label>
          <input
            value={signature}
            onChange={(e) => setSignature(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs mb-3"
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
          <div className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs break-all">
            {result}
          </div>
        </div>
      )}
    </div>
  );
}

export default RSATools;