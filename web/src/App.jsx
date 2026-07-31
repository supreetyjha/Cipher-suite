import { useState } from "react";
import { encryptCaesar, decryptCaesar } from "./api/client";

function App() {
  const [text, setText] = useState("");
  const [shift, setShift] = useState(3);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handle(action) {
    setError("");
    setResult("");
    setLoading(true);
    try {
      const data = action === "encrypt"
        ? await encryptCaesar(text, Number(shift))
        : await decryptCaesar(text, Number(shift));
      setResult(data.result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 font-mono flex items-center justify-center px-4">
      <div className="w-full max-w-md border border-neutral-800 rounded-md p-6">
        <h1 className="text-lg mb-1 text-neutral-100">Cipher Suite</h1>
        <p className="text-xs text-neutral-500 mb-6">Caesar Cipher</p>

        <label className="block text-xs text-neutral-500 mb-1">Text</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={3}
          className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-4 focus:outline-none focus:border-neutral-600"
        />

        <label className="block text-xs text-neutral-500 mb-1">Shift (0-25)</label>
        <input
          type="number"
          min={0}
          max={25}
          value={shift}
          onChange={(e) => setShift(e.target.value)}
          className="w-24 bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-4 focus:outline-none focus:border-neutral-600"
        />

        <div className="flex gap-2 mb-4">
          <button
            onClick={() => handle("encrypt")}
            disabled={loading || !text}
            className="flex-1 bg-neutral-100 text-neutral-900 text-sm rounded px-3 py-2 disabled:opacity-40"
          >
            Encrypt
          </button>
          <button
            onClick={() => handle("decrypt")}
            disabled={loading || !text}
            className="flex-1 border border-neutral-700 text-sm rounded px-3 py-2 disabled:opacity-40"
          >
            Decrypt
          </button>
        </div>

        {error && <p className="text-xs text-red-400 mb-2">{error}</p>}

        {result && (
          <div>
            <label className="block text-xs text-neutral-500 mb-1">Result</label>
            <div className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm break-all">
              {result}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;