import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def analyze_html_content(url):
    """
    Fetches the HTML of the URL and performs simple heuristic checks:
    - Looks for password input fields (login forms)
    - Counts external links
    - Looks for hidden elements
    """
    results = {
        'has_login_form': 0,
        'external_links_count': 0,
        'hidden_elements_count': 0,
        'fetch_error': False
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # 5-second timeout to prevent hanging on bad sites
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Detect password forms
        password_inputs = soup.find_all('input', type='password')
        if len(password_inputs) > 0:
            results['has_login_form'] = 1

        # 2. Count external links (links going outside the base domain)
        domain = urlparse(url).netloc
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith('http') and domain not in urlparse(href).netloc:
                results['external_links_count'] += 1

        # 3. Detect hidden elements
        hidden_elements = soup.find_all(style=lambda value: value and ('display: none' in value or 'visibility: hidden' in value))
        results['hidden_elements_count'] = len(hidden_elements)

    except requests.exceptions.RequestException:
        # Could not fetch content securely
        results['fetch_error'] = True

    return results
