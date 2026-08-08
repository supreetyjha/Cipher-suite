import { useState } from "react";
import {
  caesarEncrypt, caesarDecrypt,
  vigenereEncrypt, vigenereDecrypt,
  playfairEncrypt, playfairDecrypt,
  railFenceEncrypt, railFenceDecrypt,
  analyzeFrequency, bruteForceCaesar,
} from "./api/client";
import ModernCrypto from "./components/ModernCrypto";
import RSATools from "./components/RSATools";
import HashingTools from "./components/HashingTools";
import ECBVisualizer from "./components/ECBVisualizer";

const CIPHERS = {
  caesar: { label: "Caesar", keyLabel: "Shift (0-25)", keyType: "number" },
  vigenere: { label: "Vigenère", keyLabel: "Key (letters)", keyType: "text" },
  playfair: { label: "Playfair", keyLabel: "Key (letters)", keyType: "text" },
  railfence: { label: "Rail Fence", keyLabel: "Rails (2-20)", keyType: "number" },
};

const TABS = ["Classical", "Modern (AES/ChaCha20)", "RSA", "Hashing", "ECB vs CBC"];

function ClassicalPanel() {
  const [cipher, setCipher] = useState("caesar");
  const [text, setText] = useState("");
  const [keyVal, setKeyVal] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [bruteResults, setBruteResults] = useState(null);
  const [freqResults, setFreqResults] = useState(null);

  const config = CIPHERS[cipher];

  async function handle(action) {
    setError(""); setResult(""); setLoading(true);
    try {
      let data;
      if (cipher === "caesar") {
        data = action === "encrypt" ? await caesarEncrypt(text, Number(keyVal)) : await caesarDecrypt(text, Number(keyVal));
      } else if (cipher === "vigenere") {
        data = action === "encrypt" ? await vigenereEncrypt(text, keyVal) : await vigenereDecrypt(text, keyVal);
      } else if (cipher === "playfair") {
        data = action === "encrypt" ? await playfairEncrypt(text, keyVal) : await playfairDecrypt(text, keyVal);
      } else if (cipher === "railfence") {
        data = action === "encrypt" ? await railFenceEncrypt(text, Number(keyVal)) : await railFenceDecrypt(text, Number(keyVal));
      }
      setResult(data.result);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleAnalyze() {
    setError(""); setFreqResults(null); setBruteResults(null); setLoading(true);
    try {
      const [freq, brute] = await Promise.all([analyzeFrequency(text), bruteForceCaesar(text)]);
      setFreqResults(freq.frequencies);
      setBruteResults(brute.attempts);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <label className="block text-xs text-neutral-500 mb-1">Cipher</label>
      <select
        value={cipher}
        onChange={(e) => { setCipher(e.target.value); setResult(""); setError(""); }}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-4"
      >
        {Object.entries(CIPHERS).map(([key, c]) => <option key={key} value={key}>{c.label}</option>)}
      </select>

      <label className="block text-xs text-neutral-500 mb-1">Text</label>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={3}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-4"
      />

      <label className="block text-xs text-neutral-500 mb-1">{config.keyLabel}</label>
      <input
        type={config.keyType}
        value={keyVal}
        onChange={(e) => setKeyVal(e.target.value)}
        className="w-full bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm mb-4"
      />

      <div className="flex gap-2 mb-2">
        <button onClick={() => handle("encrypt")} disabled={loading || !text || !keyVal} className="flex-1 bg-neutral-100 text-neutral-900 text-sm rounded px-3 py-2 disabled:opacity-40">Encrypt</button>
        <button onClick={() => handle("decrypt")} disabled={loading || !text || !keyVal} className="flex-1 border border-neutral-700 text-sm rounded px-3 py-2 disabled:opacity-40">Decrypt</button>
      </div>

      {cipher === "caesar" && (
        <button onClick={handleAnalyze} disabled={loading || !text} className="w-full border border-neutral-800 text-xs text-neutral-400 rounded px-3 py-2 mb-4 disabled:opacity-40">
          Run Frequency Analysis + Brute Force
        </button>
      )}

      {error && <p className="text-xs text-red-400 mb-2">{error}</p>}

      {result && (
        <div className="mb-4">
          <label className="block text-xs text-neutral-500 mb-1">Result</label>
          <div className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-sm break-all">{result}</div>
        </div>
      )}

      {freqResults && (
        <div className="mb-4">
          <label className="block text-xs text-neutral-500 mb-1">Letter Frequency (%)</label>
          <div className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs flex flex-wrap gap-x-3 gap-y-1">
            {Object.entries(freqResults).map(([letter, pct]) => <span key={letter}>{letter}: {pct}%</span>)}
          </div>
        </div>
      )}

      {bruteResults && (
        <div>
          <label className="block text-xs text-neutral-500 mb-1">Brute Force (all 26 shifts)</label>
          <div className="bg-neutral-900 border border-neutral-800 rounded px-3 py-2 text-xs max-h-40 overflow-y-auto space-y-0.5">
            {bruteResults.map(({ shift, result }) => (
              <div key={shift}><span className="text-neutral-600">{shift}:</span> {result}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 font-mono flex items-start justify-center px-4 py-10">
      <div className="w-full max-w-lg border border-neutral-800 rounded-md p-6">
        <h1 className="text-lg mb-1 text-neutral-100">Cipher Suite</h1>
        <p className="text-xs text-neutral-500 mb-4">Classical &amp; Modern Cryptography Toolkit</p>

        <div className="flex flex-wrap gap-1 mb-6 border-b border-neutral-800 pb-3">
          {TABS.map((tab, i) => (
            <button
              key={tab}
              onClick={() => setActiveTab(i)}
              className={`text-xs px-2 py-1 rounded ${
                activeTab === i ? "bg-neutral-100 text-neutral-900" : "text-neutral-500 hover:text-neutral-300"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 0 && <ClassicalPanel />}
        {activeTab === 1 && <ModernCrypto />}
        {activeTab === 2 && <RSATools />}
        {activeTab === 3 && <HashingTools />}
        {activeTab === 4 && <ECBVisualizer />}
      </div>
    </div>
  );
}

export default App;