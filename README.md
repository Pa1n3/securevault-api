# SecureVault API

A production-ready REST API built with Python and FastAPI, demonstrating secure authentication, role-based access control, and real-world security implementations. Built as a portfolio project showcasing backend development and security engineering skills.

---

## Features

- **JWT Authentication** — secure token-based auth with expiry
- **Role-Based Access Control** — user and admin roles with protected routes
- **Password Security** — argon2 hashing, reset flow with expiring tokens
- **IDOR Protection** — ownership verification on all resource access
- **Rate Limiting** — brute force protection on authentication endpoints
- **File Upload** — extension whitelisting, size limits, UUID-safe filenames
- **Input Validation** — schema-level validation on all incoming data
- **Error Handling** — consistent JSON error responses across all endpoints

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Database | PostgreSQL |
| Authentication | JWT (PyJWT) |
| Password Hashing | Argon2 |
| Rate Limiting | SlowAPI |
| Validation | Pydantic |

---

## Security Implementations

| Vulnerability | Implementation |
|---|---|
| SQL Injection | Parameterized queries throughout |
| Brute Force | Rate limiting — 5 attempts/minute on login |
| IDOR | Ownership check on every resource query |
| Weak Passwords | Minimum length + pattern validation |
| Plaintext Passwords | Argon2 hashing — never stored in plaintext |
| Privilege Escalation | Role verification on every admin route |
| Unsafe File Upload | Extension whitelist + UUID filename generation |
| Info Leakage | Generic error messages on auth failures |
| Token Forgery | JWT signature verification + algorithm pinning |
| Unlimited Reset | One-time use tokens with 10 minute expiry |

---

## Project Structure

```
securevault-api/
├── app/
│   ├── main.py          # app entry point, middleware
│   ├── database.py      # PostgreSQL connection + query executor
│   ├── models.py        # table definitions
│   ├── schemas.py       # request/response validation
│   ├── auth.py          # JWT + password logic
│   ├── errors.py        # custom exception handlers
│   ├── limiter.py       # rate limiting configuration
│   └── routers/
│       ├── users.py     # auth endpoints
│       ├── notes.py     # notes CRUD
│       └── files.py     # file upload
├── uploads/
├── .env
└── requirements.txt
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/Pa1n3/securevault-api
cd securevault-api
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

**5. Set up PostgreSQL**
```sql
CREATE DATABASE securevault;
CREATE USER vaultuser WITH PASSWORD 'yourpassword';
GRANT ALL ON SCHEMA public TO vaultuser;
```

**6. Run the server**
```bash
uvicorn app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/users/register` | No | Create account |
| POST | `/users/login` | No | Get JWT token |
| GET | `/users/me` | Yes | Your profile |
| POST | `/users/forgot-password` | No | Request reset token |
| POST | `/users/reset-password` | No | Reset with token |

### Notes
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/notes/` | Yes | Create note |
| GET | `/notes/` | Yes | Your notes |
| GET | `/notes/{id}` | Yes | Single note (owner only) |
| PUT | `/notes/{id}` | Yes | Update note |
| DELETE | `/notes/{id}` | Yes | Delete note |
| GET | `/notes/admin/all` | Admin | All notes |

### Files
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/files/upload` | Yes | Upload file |
| GET | `/files/` | Yes | Your files |

---

## Security Notes

This project was built with a security-first mindset. Every feature was designed by first asking: *"How could this be exploited?"*

Key decisions:
- Rate limiting applied specifically to login, not globally, to avoid false positives
- Reset tokens are single-use and expire in 10 minutes — preventing token reuse attacks
- File uploads use UUID-generated names — preventing path traversal via filename manipulation
- Auth errors always return identical messages — preventing username enumeration
- JWT algorithm is hardcoded server-side — preventing algorithm confusion attacks

---

## Author

**Sandro** — IT Specialist & Backend Developer  
Focused on building secure APIs and systems with Python.

---
