from flask import Flask, render_template, request, redirect, url_for
import pandas as pd  # only if you still show dataset stats anywhere; otherwise you can remove
from nltk import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path
import joblib

# -------------------- Load persisted artifacts --------------------
APP_DIR   = Path(__file__).parent
VECT_PATH = APP_DIR / "vect.joblib"
MODEL_PATH= APP_DIR / "model.joblib"

# Load the trained vectorizer + model
vectorizer: CountVectorizer      = joblib.load(VECT_PATH)
model: LogisticRegression        = joblib.load(MODEL_PATH)

# Same text processing used when training
tokenizer = RegexpTokenizer(r"[A-Za-z]+")
stemmer   = SnowballStemmer("english")

def stem_text(s: str) -> str:
    return " ".join(stemmer.stem(t) for t in tokenizer.tokenize(str(s)))

# Build coef lookup for token “influence” chips
feature_names = vectorizer.get_feature_names_out()
coefs = model.coef_[0]  # + => pushes GOOD(1), - => pushes BAD(0)
coef_map = {w: float(c) for w, c in zip(feature_names, coefs)}

# -------------------- Flask --------------------
app = Flask(__name__)

def featurize_url(raw_url: str):
    tokens = tokenizer.tokenize(raw_url)
    stems  = [stemmer.stem(t) for t in tokens]
    text   = " ".join(stems)
    X      = vectorizer.transform([text])
    return X, tokens, stems

def top_cues(stems, k=6, for_pred_bad=False):
    scored = [(tok, coef_map.get(tok, 0.0)) for tok in stems if tok in coef_map]
    if not scored:
        return []
    # good => show highest weights first; bad => show lowest weights first
    scored.sort(key=lambda x: x[1], reverse=not for_pred_bad)
    return scored[:k]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            return render_template("index.html", flash_msg="Please enter a URL.")
        if len(url) > 2048:
            return render_template("index.html", flash_msg="URL is too long.")

        X, tokens, stems = featurize_url(url)
        proba_good = float(model.predict_proba(X)[0, 1])
        proba_bad  = 1.0 - proba_good
        pred_is_good = proba_good >= 0.5

        status = "good" if pred_is_good else "bad"
        label_text = "GOOD (1)" if pred_is_good else "BAD (0)"
        confidence = proba_good if pred_is_good else proba_bad
        cues = top_cues(stems, k=6, for_pred_bad=not pred_is_good)

        cue_items = [{"token": t, "weight": w} for t, w in cues]

        return render_template(
            "index.html",
            input_url=url,
            status=status,
            label_text=label_text,
            confidence=f"{confidence*100:.1f}",
            prob_good=f"{proba_good*100:.1f}",
            prob_bad=f"{proba_bad*100:.1f}",
            cues=cue_items,
        )
    return render_template("index.html")

@app.route("/predict")
def predict_redirect():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # avoid double-loading in debug
