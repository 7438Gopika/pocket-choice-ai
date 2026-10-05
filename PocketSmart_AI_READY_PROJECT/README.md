# PocketSmart AI

Complete FastAPI + Jinja2 implementation of the supplied PocketSmart AI documentation. This version is organized as a ready-to-run college/demo project and includes Home, Party, Jewelry, authentication, history, catalog links, Gemini integration, and deterministic fallback logic.

## Features
- Home, Party and Jewelry budget planners
- Gemini structured recommendations with optional outfit image input
- Deterministic fallback recommendations if Gemini is not configured/unavailable
- Mock/seed catalog with links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO
- Registration, scrypt password hashing, session cookies and JWT `/token`
- Recommendation history and detail API
- Responsive frontend
- Pytest suite

## Setup in VS Code (Windows)
```powershell
cd PocketSmart_AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
If activation is blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

Edit `.env` and optionally add `GEMINI_API_KEY=...`. Default model is `gemini-2.5-flash`; change `GEMINI_MODEL` if needed.

Run:
```powershell
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

Test:
```powershell
pytest -q
```

## API
`POST /register`, `POST /login`, `POST /logout`, `POST /token`, `GET /session-info`, `GET /session-data`, `POST /generate-home`, `POST /generate-party`, `POST /generate-jewelry`, `GET /recommendations-details/{id}`, `GET /history`, `GET /health`.

The external platforms are represented by local mock catalog data and search URLs rather than undocumented scraping/private APIs. For production, replace the catalog with authorized APIs/affiliate feeds, use PostgreSQL, HTTPS, stronger secret management, rate limiting, and object storage for images.
