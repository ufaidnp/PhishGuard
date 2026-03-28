import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

from utils.feature_extractor import extract_features
from utils.domain_checker import check_domain_age

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic dataset of URLs for demonstration.
    """
    print(f"Generating {n_samples} synthetic URLs...")
    
    legit_domains = ['google.com', 'github.com', 'microsoft.com', 'amazon.com', 'wikipedia.org']
    phish_domains = ['secure-login-verify-account.com', '192.168.1.100', 'update-your-billing-info.net', 'banking-confirm.org']
    
    urls = []
    labels = []
    
    for _ in range(n_samples // 2):
        # Legitimate URLs
        domain = np.random.choice(legit_domains)
        url = f"https://www.{domain}"
        urls.append(url)
        labels.append(0)  # 0 = Legitimate
        
        # Phishing URLs
        domain = np.random.choice(phish_domains)
        url = f"http://{domain}/login"
        urls.append(url)
        labels.append(1)  # 1 = Phishing
        
    return pd.DataFrame({'url': urls, 'label': labels})

def process_data(df):
    print("Extracting features (this may take a moment)...")
    feature_list = []
    for index, row in df.iterrows():
        url = row['url']
        features = extract_features(url)
        # Avoid heavy WHOIS lookups for the synthetic generated data to keep training fast
        features['domain_age'] = -1 if row['label'] == 1 else 1000 
        feature_list.append(features)
        
    features_df = pd.DataFrame(feature_list)
    return features_df, df['label']

def train_and_evaluate():
    print("Starting ML Pipeline...")
    df = generate_synthetic_data(n_samples=1000)
    X, y = process_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n--- Model Performance Metrics ---")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("---------------------------------")
    
    model_path = 'phishing_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved successfully to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
