import whois
from datetime import datetime

def check_domain_age(domain):
    """
    Checks WHOIS record to determine the age of the domain in days.
    Newly registered domains are a common vector for phishing attacks.
    """
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        
        # WHOIS might return a list of dates, we take the earliest one
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            age = (datetime.now() - creation_date).days
            return max(age, 0)
        return -1 # Indicates creation date is unknown or missing
    except Exception:
        # WHOIS query failed (e.g., domain doesn't exist, timeout, or blocked)
        return -1
