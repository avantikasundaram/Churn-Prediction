# ChurnShield AI — Local Development Setup

## Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

### 3. Login
- **Email**: admin@churnshield.ai  
- **Password**: Admin@123  
- **Role**: Admin

---

## What Was Fixed

| File | Fix |
|------|-----|
| `frontend/.env` | Changed `VITE_API_BASE_URL` to empty — local dev now uses the Vite proxy to reach `localhost:5000` instead of the remote Render URL |
| `frontend/src/services/api.js` | `BASE_URL` defaults to `''` (empty) so Vite proxy forwards `/api/*` correctly |
| `backend/app.py` | CORS now allows `http://localhost:5173` and `http://localhost:3000` in addition to the production URL |
| `backend/app.py` | `/api/auth/login` now uses **fallback auth** (env-var credentials) when MongoDB is unreachable — login works offline |
| `backend/auth.py` | Added `verify_login_fallback()` that validates against `ADMIN_EMAIL`/`ADMIN_PASSWORD` from `.env` without needing MongoDB |
| `backend/database.py` | Clearer connection error messages with an actionable checklist (IP whitelist, credentials, paused cluster) |
| `frontend/src/pages/Login.jsx` | Better error messages — distinguishes "backend not running" from "MongoDB error" |

## MongoDB Atlas: If You Still See DB Errors

1. Go to [Atlas Console](https://cloud.mongodb.com) → **Network Access**
2. Click **Add IP Address** → **Allow Access from Anywhere** (`0.0.0.0/0`) for dev
3. Restart the backend

## Production Deployment
Set `VITE_API_BASE_URL=https://your-backend.onrender.com` in your hosting environment's env vars (not in `frontend/.env`).
