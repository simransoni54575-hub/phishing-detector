from flask import Flask, render_template, request
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Trusted domains list
trusted_domains = [
    "google.com",
    "youtube.com",
    "github.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "openai.com",
    "wikipedia.org",
    "netflix.com",
    "whatsapp.com"
]

# Suspicious keywords
suspicious_keywords = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "free",
    "gift",
    "bonus",
    "crypto",
    "win",
    "claim",
    "password",
    "wallet",
    "paypal",
    "account",
    "signin"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url'].strip().lower()

    # Add https automatically if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove www.
    if domain.startswith("www."):
        domain = domain.replace("www.", "")

    # URL validation
    regex = re.compile(
        r'^(https?:\/\/)'
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
        r'(\/.*)?$'
    )

    # INVALID URL
    if not regex.match(url):

        result = "Invalid URL ⚠️"
        color = "orange"

    # TRUSTED WEBSITE
    elif domain in trusted_domains:

        result = "Safe Website ✅"
        color = "green"

    else:

        phishing_score = 0

        # Long URL
        if len(url) > 75:
            phishing_score += 1

        # @ symbol
        if "@" in url:
            phishing_score += 2

        # Too many hyphens
        if url.count("-") >= 2:
            phishing_score += 1

        # IP address check
        ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        if ip_pattern.search(url):
            phishing_score += 2

        # Suspicious words
        for word in suspicious_keywords:
            if word in url:
                phishing_score += 1

        # Fake domains
        fake_domains = [
            ".tk",
            ".xyz",
            ".ru",
            ".top",
            ".gq",
            ".ml",
            ".cf"
        ]

        for fd in fake_domains:
            if domain.endswith(fd):
                phishing_score += 2

        # HTTPS missing
        if not url.startswith("https://"):
            phishing_score += 1

        # Final Decision
        if phishing_score >= 3:
            result = "Phishing Website ❌"
            color = "red"

        elif phishing_score == 2:
            result = "Suspicious Website ⚠️"
            color = "orange"

        else:
            result = "Safe Website ✅"
            color = "green"

    return render_template(
        'index.html',
        result=result,
        color=color
    )


if __name__ == "__main__":
    app.run(debug=True)
