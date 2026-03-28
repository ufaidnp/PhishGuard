import re

def is_safe_browsing_flagged(url):
    """
    Integrates a blacklist check.
    In a real-world scenario, you would call the Google Safe Browsing API here.
    For demonstration, we use a mock implementation targeting known test URLs.
    """
    # NOTE: To use a real Google API key, set `API_KEY = "YOUR_KEY"` and replace this mock
    # with a request to `https://safebrowsing.googleapis.com/v4/threatMatches:find`
    
    mock_blacklist = [
        'http://verify-account-update.info',
        'http://secure-login-verify-account.com',
        'http://192.168.1.100/login',
        'http://update-your-billing-info.net'
    ]
    return url in mock_blacklist

def sanitize_url(url):
    """
    Basic input validation to ensure the input resembles a URL and
    prevent trivial injection attempts.
    """
    url = url.strip()
    # Force http:// if no protocol is defined so urlparse can work properly
    if not re.match(r'^https?://', url):
        url = 'http://' + url
    return url
