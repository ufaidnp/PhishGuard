import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

from utils.feature_extractor import extract_features
from utils.domain_checker import check_domain_age
from utils.content_analyzer import analyze_html_content
from utils.security import sanitize_url, is_safe_browsing_flagged
import tldextract

app = Flask(__name__)

# Load the trained ML model globally
MODEL_PATH = 'phishing_model.pkl'
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Warning: Model file not found at {MODEL_PATH}. Prediction via ML will fail unless trained.")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
        
    raw_url = data['url']
    url = sanitize_url(raw_url)
    
    # 1. Threat Intelligence Check
    if is_safe_browsing_flagged(url):
        return jsonify({
            'result': 'Phishing',
            'confidence': 99.99,
            'details': 'URL is flagged by Google Safe Browsing blacklist.'
        })
        
    # 2. URL Feature Extraction for ML Model
    features = extract_features(url)
    ext = tldextract.extract(url)
    features['domain_age'] = check_domain_age(ext.domain)
    
    # 3. Model Prediction
    if model:
        # Simple rule-based detection (no ML)
if "@" in url or len(url) > 75 or "login" in url:
    result_text = "Phishing"
    confidence = 80.0
    details_text = "Rule-based detection: suspicious URL pattern."
else:
    result_text = "Legitimate"
    confidence = 90.0
    details_text = "URL appears safe based on simple checks."
    else:
        # Fallback mechanism
        is_phishing = features['suspicious_keywords_count'] > 0 or features['is_ip_address']
        result_text = "Phishing" if is_phishing else "Legitimate"
        confidence = 80.0
        details_text = "Fallback rules applied. Model not found."
    
    # 4. Optional Context: HTML content heuristics
    html_stats = analyze_html_content(url)
    
    # Send all details to UI
    return jsonify({
        'result': result_text,
        'confidence': round(confidence, 2),
        'details': details_text,
        'features': features,
        'html_analysis': html_stats
    })

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host="0.0.0.0", port=10000)
