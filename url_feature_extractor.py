import re
from urllib.parse import urlparse
from datetime import datetime
import whois

def manual_feature_extraction(url):
    features = []

    def get_domain(url):
        try:
            return urlparse(url).netloc
        except:
            return ""

    def get_whois_data(domain):
        try:
            return whois.whois(domain)
        except:
            return None

    def domain_age_in_days(whois_data):
        try:
            creation_date = whois_data.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            return (datetime.now() - creation_date).days
        except:
            return -1

    # Feature 1: Having IP Address
    match = re.search(r'(([0-9]{1,3}\.){3}[0-9]{1,3})', url)
    features.append(1 if match else -1)

    # Feature 2: URL Length
    if len(url) < 54:
        features.append(-1)
    elif 54 <= len(url) <= 75:
        features.append(0)
    else:
        features.append(1)

    # Feature 3: Shortening Service
    shorteners = r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|buff\.ly"
    features.append(1 if re.search(shorteners, url) else -1)

    # Feature 4: Having '@' symbol
    features.append(1 if '@' in url else -1)

    # Feature 5: Double slash redirecting
    features.append(1 if url.count('//') > 1 else -1)

    # Feature 6: Prefix-Suffix in domain
    domain = get_domain(url)
    features.append(1 if '-' in domain else -1)

    # Feature 7: Subdomain count
    dot_count = domain.count('.')
    if dot_count == 1:
        features.append(-1)
    elif dot_count == 2:
        features.append(0)
    else:
        features.append(1)

    # Feature 8: SSL final state (HTTPS check)
    features.append(-1 if url.startswith("https") else 1)

    # Feature 9: Domain registration length (WHOIS)
    whois_data = get_whois_data(domain)
    if whois_data is None:
        features.append(1)  # suspicious
    else:
        age = domain_age_in_days(whois_data)
        features.append(1 if age < 180 else -1)  # less than 6 months → suspicious

    # Feature 10–30: Placeholder dummy (safe value)
    for _ in range(21):  # already 9 features above
        features.append(0)

    return features
