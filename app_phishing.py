# Step 1: Imports
from flask import Flask, render_template, request
import joblib
import numpy as np
import re
from urllib.parse import urlparse

# Step 2: Flask App and Load Models
app = Flask(__name__)
phish_model = joblib.load("phishing_model.pkl")
spam_model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Helper Function: Check if text is a URL
def is_url(text):
    return bool(re.match(r'^https?://|www\.', text))

# Step 3: Feature Extraction (30 Features for Phishing URL)
def manual_feature_extraction(url):
    features = []

    def get_domain(url):
        try:
            return urlparse(url).netloc
        except:
            return ""

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

    # Feature 8: SSL (https used or not)
    features.append(-1 if url.startswith("https") else 1)

    # Features 9–30: Dummy (Placeholder)
    for _ in range(22):
        features.append(1)

    return features

# Step 4: Flask Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    prediction = None
    if request.method == 'POST':
        input_text = request.form['input_text'].strip()

        if is_url(input_text):
            # 🔧 Add protocol if missing
            if not input_text.startswith(('http://', 'https://')):
                input_text = 'https://' + input_text

            # 🧠 Check for known suspicious domains
            suspicious_domains = [
                "rummycircle.com", "winzogames.com",
                "ludo99.com", "loot247.net",
                "dream11-bonus.xyz", "rummyinapp.net"
            ]
            if any(domain in input_text.lower() for domain in suspicious_domains):
                prediction = "🚨 Phishing Website (Known Suspicious Domain)"
            else:
                features = manual_feature_extraction(input_text)
                if features is None or len(features) != 30:
                    prediction = "⚠️ Could not extract proper features from the URL."
                else:
                    result = phish_model.predict([features])[0]
                    prediction = "🚨 Phishing Website" if result == 1 else "✅ Legitimate Website"
        else:
            # 📩 Email spam detection
            text_vector = vectorizer.transform([input_text])
            result = spam_model.predict(text_vector)[0]
            prediction = "🚫 Spam Email" if result == 1 else "📩 Legitimate Email"

    return render_template("detect.html", prediction=prediction)



# Step 5: Run App
if __name__ == '__main__':
    app.run(debug=True)

