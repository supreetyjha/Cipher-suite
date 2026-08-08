# 🔐 Cipher Suite

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/frontend-React-61DAFB.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A full-stack cryptography toolkit spanning classical ciphers, cryptanalysis tools, and modern encryption primitives — built to demonstrate both cryptographic understanding and production-grade software architecture.

**🔗 Live demo:** [cipher-suite.vercel.app](https://cipher-suite.vercel.app)
**⚙️ API docs:** [cipher-suite.onrender.com/docs](https://cipher-suite.onrender.com/docs)

> The backend runs on a free-tier server that spins down after inactivity. The first request after idle time may take 30–50 seconds while it wakes up — a hosting limitation, not an application bug.

<!-- Optional: add a GIF or screenshot here once recorded -->
<!-- ![Cipher Suite demo](docs/demo.gif) -->

---

## Features

### Classical Ciphers & Cryptanalysis
| Cipher | Encrypt/Decrypt | Notes |
|---|---|---|
| Caesar | ✅ | Includes brute-force cracking (all 26 shifts) |
| Vigenère | ✅ | Polyalphabetic, keyword-based |
| Playfair | ✅ | 5×5 grid digraph substitution |
| Rail Fence | ✅ | Transposition cipher |
| Frequency Analysis | ✅ | Letter-frequency breakdown for any text |

### Modern Cryptography
| Primitive | Status | Details |
|---|---|---|
| AES-256 | ✅ | ECB, CBC, CFB, OFB, GCM modes |
| ChaCha20 | ✅ | Stream cipher |
| RSA-2048 | ✅ | Key generation, encrypt/decrypt, sign/verify |
| Argon2 | ✅ | Password hashing with automatic per-hash salting |
| SHA-256 / SHA-512 | ✅ | Digest computation |
| Argon2 KDF | ✅ | Passphrase-based key derivation |

### Interactive Tools
- **ECB vs. CBC Visualizer** — encrypts repeated plaintext blocks under both modes and renders each ciphertext block as a color swatch, visually demonstrating why ECB leaks structural patterns and CBC does not.

---

## Why this project

Most "Caesar cipher" projects stop at a CLI script. This one is built to show the difference between an educational exercise and a working system:

- **Classical ciphers** are implemented from scratch to demonstrate understanding of string manipulation, modular arithmetic, and the substitution/transposition principles underlying all cryptography.
- **Modern cryptography** (AES, RSA, ChaCha20, Argon2) uses audited, industry-standard libraries (`cryptography`, `PyCryptodome`, `argon2-cffi`) rather than hand-rolled implementations — knowing *not* to reinvent cryptographic primitives is itself a security-relevant decision.
- **ChaCha20 is intentionally unauthenticated** in this implementation to illustrate the difference between confidentiality and integrity — the test suite documents that decrypting with the wrong key produces garbage rather than an error, which is exactly why real systems pair it with Poly1305 (ChaCha20-Poly1305 AEAD).
- The **architecture separates business logic from delivery mechanism**: the core cipher engine has zero dependency on FastAPI, HTTP, or any framework, so it's independently testable and reusable across a CLI, an API, or any future interface.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.11 |
| Frontend | React, Vite, Tailwind CSS |
| Cryptography | `cryptography`, `PyCryptodome`, `argon2-cffi` |
| Testing | pytest (30+ tests) |
| Linting | Ruff (Python), ESLint (JavaScript) |
| CI/CD | GitHub Actions |
| Hosting | Render (backend), Vercel (frontend) |

---

## Architecture

Three layers, cleanly separated so logic, delivery, and presentation never bleed into one another:

```
┌─────────────────────────────────────────┐
│  Frontend (React + Vite)                 │  → user interaction, visualizations
└──────────────────┬────────────────────────┘
                   │ REST (JSON over HTTPS)
┌──────────────────▼────────────────────────┐
│  Backend API (FastAPI)                     │  → validation, routing, orchestration
└──────────────────┬────────────────────────┘
                   │ function calls
┌──────────────────▼────────────────────────┐
│  Core crypto engine (pure Python package)  │  → all cipher logic, no I/O, no framework
└─────────────────────────────────────────────┘
```

The core engine is importable standalone with zero knowledge of HTTP or any framework — the same logic powers the API and the full test suite without duplication.

### Project structure

```
cipher-suite/
├── core/                          # pure logic, no framework deps
│   ├── classical/                 # caesar.py, vigenere.py, playfair.py, rail_fence.py
│   ├── symmetric/                 # aes.py, chacha20.py
│   ├── asymmetric/                # rsa.py
│   ├── hashing/                   # digest.py, password.py
│   ├── analysis/                  # frequency.py, brute_force.py
│   ├── kdf.py
│   └── exceptions.py              # custom exception hierarchy
│
├── api/                           # FastAPI layer
│   ├── main.py                    # app init, CORS, router mounting
│   ├── routers/                   # one router per cipher family
│   └── schemas/                   # Pydantic request/response models
│
├── cli.py                         # thin CLI wrapper around core/
│
├── web/                           # React frontend (separate deploy)
│   └── src/
│       ├── components/            # ModernCrypto, RSATools, HashingTools, ECBVisualizer
│       ├── api/client.js          # fetch wrapper for backend
│       └── App.jsx
│
├── tests/
│   └── core/                      # unit tests, mirrors core/ structure
│
├── .github/workflows/ci.yml       # lint + test on every push
├── requirements.txt
├── pyproject.toml
└── .python-version
```

**Design decisions:**
- Each cipher family is its own module — adding a new cipher means adding a file, not editing existing ones.
- Custom exceptions (`InvalidKeyError`, `UnsupportedModeError`, `DecryptionError`) instead of bare `ValueError`s, so the API layer maps errors to correct HTTP status codes.
- Frontend and backend are deployed and scaled independently — standard practice for real-world full-stack systems.
- All keys/IVs/nonces/tags are base64-encoded at the API boundary for safe JSON transport.

---

## API Examples

**Caesar cipher**
```bash
curl -X POST https://cipher-suite.onrender.com/classical/caesar/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "shift": 3}'
# → {"result": "khoor"}
```

**AES-256-GCM**
```bash
# 1. Generate a key
curl https://cipher-suite.onrender.com/symmetric/aes/generate-key

# 2. Encrypt
curl -X POST https://cipher-suite.onrender.com/symmetric/aes/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "top secret", "key": "<generated-key>", "mode": "GCM"}'
# → {"ciphertext": "...", "iv": "...", "tag": "..."}
```

**RSA sign & verify**
```bash
curl https://cipher-suite.onrender.com/asymmetric/rsa/generate-keypair

curl -X POST https://cipher-suite.onrender.com/asymmetric/rsa/sign \
  -H "Content-Type: application/json" \
  -d '{"message": "authentic message", "private_key": "<pem>"}'
# → {"signature": "..."}
```

**Argon2 password hashing**
```bash
curl -X POST https://cipher-suite.onrender.com/hashing/password/hash \
  -H "Content-Type: application/json" \
  -d '{"password": "correct-horse-battery-staple"}'
# → {"hashed": "$argon2id$v=19$m=65536,t=3,p=4$..."}
```

Full interactive documentation with all endpoints: [cipher-suite.onrender.com/docs](https://cipher-suite.onrender.com/docs)

---

## Running locally

**Backend**
```bash
git clone https://github.com/supreetyjha/cipher-suite.git
cd cipher-suite
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
# source venv/bin/activate        # macOS/Linux

pip install -r requirements.txt
uvicorn api.main:app --reload
```
API runs at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`.

**Frontend**
```bash
cd web
npm install
npm run dev
```
Site runs at `http://localhost:5173`.

---

## Testing

```bash
pytest tests/ -v
```
30+ tests covering encrypt/decrypt round-trips, invalid-input handling, and security-relevant edge cases — including a test that documents ECB's block-pattern leak and a test proving Argon2 produces different hashes for the same password (salting verification).

## Linting

```bash
ruff check .            # Python
cd web && npm run lint  # JavaScript/React
```

---

## Security notes

- Modern cryptographic primitives (AES, RSA, ChaCha20, Argon2) are implemented using audited libraries (`cryptography`, `PyCryptodome`, `argon2-cffi`) — never hand-rolled.
- Classical ciphers (Caesar, Vigenère, Playfair, Rail Fence) are for educational/demonstration purposes only and are not cryptographically secure by modern standards.
- ECB mode is intentionally included and exposed via the visualizer specifically to demonstrate why it should not be used in production — see the ECB vs. CBC tab in the live demo.
- ChaCha20 as implemented here provides confidentiality but not authentication; production systems should use ChaCha20-Poly1305 (AEAD).

---

## Roadmap

- [x] Project architecture & CI pipeline
- [x] Caesar, Vigenère, Playfair, Rail Fence ciphers
- [x] Frequency analysis & brute-force cracking
- [x] Password hashing with Argon2 (salting included)
- [x] Key derivation (Argon2 KDF from passphrase)
- [x] AES (ECB, CBC, CFB, OFB, GCM modes)
- [x] ChaCha20 stream cipher
- [x] RSA (key generation, encrypt/decrypt, sign/verify)
- [x] Interactive ECB vs. CBC mode visualizer
- [ ] Dockerized deployment
- [ ] Hybrid encryption demo (RSA + AES, TLS-style)

---

## License

MIT
