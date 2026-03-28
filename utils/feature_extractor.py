import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    """
    Extracts numerical features from a given URL for machine learning classification.
    """
    features = {}
    
    # 1. URL Length
    features['url_length'] = len(url)
    
    # 2. Number of subdomains
    ext = tldextract.extract(url)
    subdomains = ext.subdomain.split('.') if ext.subdomain else []
    features['num_subdomains'] = len(subdomains)
    
    # 3. Presence of @ symbol (often used to obscure the true domain)
    features['has_at_symbol'] = 1 if '@' in url else 0
    
    # 4. HTTPS usage
    parsed_url = urlparse(url)
    features['uses_https'] = 1 if parsed_url.scheme == 'https' else 0
    
    # 5. Suspicious keywords in the URL
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update', 'banking', 'confirm']
    features['suspicious_keywords_count'] = sum(1 for keyword in suspicious_keywords if keyword in url.lower())
    
    # 6. IP address instead of domain
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    features['is_ip_address'] = 1 if ip_pattern.match(ext.domain) else 0

    return features

def get_feature_names():
    # Helper to return feature keys in a consistent order
    return ['url_length', 'num_subdomains', 'has_at_symbol', 
            'uses_https', 'suspicious_keywords_count', 'is_ip_address']
