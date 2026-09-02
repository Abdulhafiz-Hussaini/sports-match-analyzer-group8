# Sports Match Analyzer & Fan Companion

A Streamlit app where users can search for a team, view upcoming fixtures
and recent results, generate AI-powered previews/summaries/trivia, bookmark
favourite teams, save notes, and get a simple fun (non-guaranteed) match
prediction.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set your Gemini API key as an environment variable before running:

```bash
export GEMINI_API_KEY="your-key-here"   # Windows: set GEMINI_API_KEY=your-key-here
```

## Run

```bash
streamlit run app.py
```

## Project structure

- `app.py` — Streamlit UI, entry point
- `sports_api_client.py` — `SportsAPIClient` class wrapping TheSportsDB API
- `team.py` — `Team` class + name cleaning (regex)
- `match.py` — `Match` class, score/date parsing (regex, datetime)
- `match_analyzer.py` — `MatchAnalyzer` class, Gemini API calls + simple prediction
- `storage.py` — local JSON file handling for favourites/notes

## Team workflow

See project branch conventions — each feature/class gets its own branch,
merged via pull request into `main`.
