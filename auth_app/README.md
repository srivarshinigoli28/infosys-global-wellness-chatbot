# FastAPI + Streamlit Auth (JWT, SQLite)

Light, minimal auth stack with:
- **FastAPI** backend (JWT auth, SQLite via SQLAlchemy, bcrypt password hashing)
- **Streamlit** frontend (no sidebar; simple top buttons; light theme)
- Endpoints: `/register`, `/login`, `/me` (GET/PUT)

## Quickstart

### 1) Create & activate a virtual environment (recommended)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2) Install deps (backend + frontend)
```bash
pip install -r requirements.txt
```

### 3) Run the API (from the `backend` folder root or project root)
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
> The SQLite DB file `app.db` will be created automatically on first run.

**Change the JWT secret!** Edit `backend/auth.py` and set `SECRET_KEY` to a long random value.

### 4) Run the Streamlit app (in another terminal)
```bash
streamlit run frontend/streamlit_app.py
```
> If your API is not on `http://127.0.0.1:8000`, set:
```bash
API_BASE=http://your-host:port streamlit run frontend/streamlit_app.py
```

## Notes
- Light theme by default (Streamlit).
- No sidebar is used; all controls are top-level.
- Minimal design intentionally: clean inputs, simple messages.
- Password updates are optional on profile page.
