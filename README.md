# 🔐 Cipher Suite

A full-stack cryptography toolkit combining classical ciphers with modern encryption primitives — built to demonstrate both cryptographic understanding and production-style software architecture.

**🔗 Live demo:** [cipher-suite.vercel.app](https://cipher-suite.vercel.app)
**⚙️ API:** [cipher-suite.onrender.com/docs](https://cipher-suite.onrender.com/docs)

> Note: the backend runs on a free-tier server that spins down after inactivity. The first request after idle time may take 30–50 seconds to respond while it wakes up — this is a hosting limitation, not an application bug.

---

## Features

**Classical Ciphers**
- ✅ Caesar cipher (encrypt/decrypt)
- ⬜ Vigenère cipher
- ⬜ Playfair cipher
- ⬜ Rail Fence cipher
- ⬜ Frequency analysis & brute-force cracking

**Modern Cryptography**
- ⬜ AES (ECB, CBC, CFB, OFB, GCM modes)
- ⬜ ChaCha20 stream cipher
- ⬜ RSA (key generation, encrypt/decrypt, sign/verify)
- ⬜ Password hashing with Argon2 (salting included)
- ⬜ Key derivation (PBKDF2 / Argon2 from passphrase)
- ⬜ Interactive ECB vs. CBC mode visualizer (demonstrates why ECB leaks patterns)

*(Checklist updates as modules are completed — see [Roadmap](#roadmap) below.)*

---

## Why this project

Most "Caesar cipher" projects stop at a CLI script. This one is built to show the difference between an educational exercise and a working system:

- **Classical ciphers** are implemented from scratch to demonstrate understanding of string manipulation, modular arithmetic, and the substitution/transposition principles that underlie all cryptography.
- **Modern cryptography** (AES, RSA, ChaCha20, Argon2) uses audited, industry-standard libraries (`cryptography`, `PyCryptodome`, `argon2-cffi`) rather than hand-rolled implementations — because knowing *not* to reinvent cryptographic primitives is itself a security-relevant decision.
- The **architecture separates business logic from delivery mechanism**: the core cipher engine has zero dependency on FastAPI, HTTP, or any framework, so it's independently testable and reusable across a CLI, an API, or any future interface.

---

## Tech Stack

| Layer       | Technology                                      |
|-------------|--------------------------------------------------|
| Backend     | FastAPI, Python 3.11                            |
| Frontend    | React, Vite, Tailwind CSS                        |
| Cryptography | `cryptography`, `PyCryptodome`, `argon2-cffi`   |
| Testing     | pytest                                           |
| Linting     | Ruff (Python), ESLint (JavaScript)               |
| CI/CD       | GitHub Actions                                   |
| Hosting     | Render (backend), Vercel (frontend)              |

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

The core engine is importable standalone and has no knowledge of HTTP or any framework — the same logic powers the API, a CLI, and the test suite without duplication.

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
│       ├── components/
│       ├── api/client.js          # fetch wrapper for backend
│       └── App.jsx
│
├── tests/
│   ├── core/                      # unit tests, mirrors core/
│   └── api/                       # endpoint tests
│
├── .github/workflows/ci.yml       # lint + test on every push
├── requirements.txt
├── pyproject.toml
└── .python-version
```

**Design decisions:**
- Each cipher family is its own module — adding a new cipher means adding a file, not editing existing ones.
- Custom exceptions (`InvalidKeyError`, `UnsupportedModeError`, `DecryptionError`) instead of bare `ValueError`s, so the API layer can map errors to correct HTTP status codes.
- Frontend and backend are deployed and scaled independently — standard practice for real-world full-stack systems.

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

## Linting

```bash
ruff check .          # Python
cd web && npm run lint  # JavaScript/React
```

---

## Roadmap

- [x] Project architecture & CI pipeline
- [x] Caesar cipher (backend + frontend, deployed)
- [ ] Vigenère, Playfair, Rail Fence ciphers
- [ ] Frequency analysis & brute-force tools
- [ ] Password hashing with Argon2
- [ ] AES (multiple modes) + ECB/CBC visual comparison
- [ ] ChaCha20 stream cipher
- [ ] RSA key generation, encryption, and signing
- [ ] Dockerized deployment

---