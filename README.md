# PocketSmart AI
Complete FastAPI + Jinja2 + SQLite + Gemini project based on the supplied PocketSmart AI documentation.

## VS Code setup (Windows)
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Terminal: `python -m venv .venv`
4. PowerShell: `.\\.venv\\Scripts\\Activate.ps1`
5. `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and add `GEMINI_API_KEY`.
7. Run `uvicorn app.main:app --reload`
8. Open `http://127.0.0.1:8000`.
9. Test: `pytest -q`.
10. API docs: `http://127.0.0.1:8000/docs`.

The supplied document names Gemini 1.5 Flash Pro. The implementation keeps the model configurable but defaults to a currently documented Gemini Flash model. Product platforms are represented by search links rather than fake live inventory or scraping.
