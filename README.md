# PhishGuard AI - Phishing Detection Application

This is a complete, production-ready AI-powered phishing detection web application built with Python (Flask) and a Random Forest classification model.

## Features

*   **URL Analysis**: Extracts numerical features (URL length, subdomain counts, HTTPS presence, etc.).
*   **Domain Intelligence**: WHOIS lookup for domain age detection via heuristics.
*   **Content Heuristics (Fallback)**: Real-time HTML DOM scanning for login forms and external links. 
*   **Machine Learning Check**: Utilizes a Random Forest classifier to identify phishing patterns across characteristics.
*   **Security Context**: Implements a mock threat intelligence blacklist mechanism (Google Safe Browsing concept).

## Project Structure

```
/phishing-detector
│
├── app.py                     # Flask server and API endpoints
├── train.py                   # Generates data and trains the RandomForest model
├── requirements.txt           # Python dependencies
├── README.md
│
├── utils/
│   ├── feature_extractor.py   # Regex and length extraction tools
│   ├── domain_checker.py      # Age verification scripts 
│   ├── content_analyzer.py    # BeautifulSoup markup parser
│   └── security.py            # Sanitizers and threat blacklists
│
├── templates/
│   └── index.html             # The responsive single-page web UI
│
├── static/
│   ├── style.css              # Dark-mode styling
│   └── script.js              # Client-side validation and fetch calls
```

## Setup Instructions

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate Dataset & Train Model**
    Initializes a synthetic dataset and builds `phishing_model.pkl`:
    ```bash
    python train.py
    ```

3.  **Run the Backend Server**
    ```bash
    python app.py
    ```
    The application will run on `http://127.0.0.1:5000`.

## Testing the Detection System

Navigate to the local server in your browser. 
Test it with the following strings:
- Legitimate Example: `https://github.com/login`
- Phishing Example (Blacklisted Mock): `http://secure-login-verify-account.com`
- Suspicious Example (Heuristics): `http://192.168.1.100/verify-account`
