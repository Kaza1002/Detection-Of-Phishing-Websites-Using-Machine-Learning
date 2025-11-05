# Detection of Phishing Websites Using Machine Learning


# 1. Executive Summary

This project presents a machine learning-based approach for detecting phishing websites through URL analysis. The model leverages Natural Language Processing (NLP) techniques and Logistic Regression to classify URLs as legitimate or malicious.
A Flask-based web interface allows users to check URLs in real time, displaying classification results, confidence levels, and interpretive feature cues. The system aims to enhance online safety awareness and minimize phishing-related risks.


# 2. Business Problem

Phishing attacks are a growing cybersecurity threat that exploit user trust by imitating legitimate websites to steal sensitive data such as passwords, credit card details, or credentials.
Traditional blacklist methods fail to detect new phishing sites promptly. The need is for an intelligent, data-driven solution that can:

Automatically analyze URLs and detect malicious intent.

Offer quick, interpretable results for both technical and non-technical users.

Serve as an educational tool to raise phishing awareness.


# 3. Methodology

Data Preparation:

Dataset: phishing_site_urls.csv containing labeled URLs as “good” or “bad.”

Tokenization: URLs are split into meaningful parts using RegexpTokenizer.

Stemming: Tokens are normalized using SnowballStemmer to reduce redundancy.

Feature Extraction: CountVectorizer converts processed text into numerical vectors for model input.

Model Development:

Algorithm: Logistic Regression, chosen for its interpretability and efficiency.

Training: Model trained on tokenized and stemmed URL data.

Evaluation: Achieved strong accuracy and recall on test data.

Persistence: Trained artifacts (model.joblib and vect.joblib) saved using Joblib for fast loading.

Web Application:

Framework: Flask

Workflow:

User submits a URL via the web interface.

The system preprocesses and vectorizes the input.

The ML model predicts if the URL is Good or Bad.

Results are shown with confidence scores, cues, and safety recommendations.


# 4. Skills

Programming: Python, HTML, CSS, Flask

Machine Learning: Logistic Regression, Text Vectorization, Tokenization

Data Handling: Pandas, NLTK, Scikit-learn

Model Deployment: Joblib model persistence, Flask app integration

Version Control: Git, GitHub


# 5. Results and Business Recommendation

The model successfully detects phishing websites with high accuracy on benchmark data.

Real-time predictions help users validate URLs instantly.

The tool provides interpretability through token-level cues that guide users toward understanding why a URL was classified as safe or unsafe.

Recommended applications:

Integration into browsers or email clients for real-time phishing detection.

Use in security training and awareness programs.

Extension into enterprise-level threat detection systems.


# 6. Next Steps

Expand dataset with real-world and multilingual phishing URLs.

Evaluate ensemble methods (Random Forest, XGBoost) for better generalization.

Deploy the app to a cloud platform such as AWS, Azure, or Render.

Add user analytics and API endpoints for automated integrations.

Implement continuous retraining with live data streams.

<!--
# 7. How to Run Locally

Prerequisites
Python 3.8 or higher
Flask, Pandas, Scikit-learn, NLTK, Joblib

Steps
# Clone the repository
git clone https://github.com/...
cd Detection-Of-Phishing-Websites-Using-Machine-Learning-

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
-->
