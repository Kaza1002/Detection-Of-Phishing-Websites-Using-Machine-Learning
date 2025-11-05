## Quick orientation for AI assistants

This repository is a small Flask-based phishing URL classifier. Keep guidance tight and code-focused: fix concrete bugs, update missing templates/data, and avoid speculative architectural rewrites.

- Entry point: `app.py` (single-process Flask server + on-start model training).
- Data: `phishing_site_urls.csv` at repository root. Expected CSV columns: `URL` and `Label` (capital `L`). Labels are textual: `good` -> 1, other -> 0.
- Templates: `Templates/` (Flask expects `index.html`). Currently this folder is empty; many features depend on an `index.html` template with a POST form field named `url` that posts to `/predict`.

Why things are structured this way
- The project trains a simple Bag-of-Words + LogisticRegression model at process start (via `CountVectorizer` + `LogisticRegression`). That keeps the code minimal but means startup time depends on dataset size and sklearn/pandas/NLTK availability.

Important code locations & patterns
- `app.py`: data preprocessing pipeline and model training. Key lines to reference:
  - CSV load (expects `URL` and `Label`) and mapping: data["Label"] -> 1/0
  - Tokenization/stemming: uses NLTK's `RegexpTokenizer` and `SnowballStemmer` to convert URLs -> token stream -> joined text.
  - Vectorizer/model: `CountVectorizer()` then `LogisticRegression(max_iter=2000)`. Model is trained on `data["Text"]` and used directly in `/predict`.

Gotchas and things to watch for (do not assume):
- Bug in CSV reading: `CSV_PATH` variable exists, but `pd.read_csv()` in `app.py` currently reads an unrelated path (`.venv/pyvenv.cfg`). Use `pd.read_csv(CSV_PATH)`.
- Templates folder is empty but `render_template("index.html")` is called. Add an `index.html` with a form like:
  - method="post", action="/predict"
  - input name="url"
- Training at startup: model training runs on import/start. For development, consider persisting a trained model (`joblib`) to avoid retraining each run; but only change this with tests/docs.
- Data sensitivity: `phishing_site_urls.csv` contains potentially sensitive URLs. Don’t exfiltrate dataset contents. If analyzing, operate locally and avoid uploading to external services.

Developer workflows
- Run locally (PowerShell):
  - Ensure a Python venv is active.
  - Install dependencies: `pip install flask pandas nltk scikit-learn` (repo currently has no `requirements.txt`).
  - Run: `python app.py` — debug mode is enabled and server is at `http://127.0.0.1:5000/`.

Automated-agent tasks (short actionable items)
- Fix CSV load: replace the incorrect `pd.read_csv(...)` argument with `CSV_PATH`.
- Add `Templates/index.html` with a minimal form that POSTs `url` to `/predict` and renders `result` variable.
- Add a `requirements.txt` with the minimal pinned dependencies: flask, pandas, nltk, scikit-learn.
- When adding changes that touch model training, include a note in the PR about training time and dataset size. Prefer small test dataset or model cache for CI.

Examples from this codebase
- Expect `Label` capitalization: the code uses `data["Label"]` and maps `str(x).lower() == "good"` to 1.
- Tokenization: `RegexpTokenizer(r"[A-Za-z]+")` and stemming via `SnowballStemmer("english")` — URL-friendly token pipeline.

Integration points & dependencies
- External libs: Flask, pandas, nltk, scikit-learn. NLTK may require downloading corpora if new tokenizers/stemmers are used (but SnowballStemmer and RegexpTokenizer do not require corpora).
- No external network APIs are called by the app code.

Conventions for AI contributors
- Make the smallest, testable change that solves a discovered bug (e.g., CSV path or missing template) and include a short PR description referencing the exact file/line changed.
- When changing model or data processing, include a short reproducible test (run on subset) and explain training-time impact.

If anything is unclear or you need missing context (example `index.html`, the expected dataset size, or CI details), ask the repo owner before making behavior-changing edits.

— end —