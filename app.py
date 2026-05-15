from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)

# Trusted Websites
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
    "netflix.com",
    "whatsapp.com",
    "wikipedia.org"
]

# Suspicious Keywords
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
    "claim",
    "winner",
    "password",
    "wallet",
    "paypal",
    "account",
    "signin",
    "otp"
]

# Dangerous Extensions
dangerous_extensions = [
    ".tk",
    ".xyz",
    ".ru",
    ".top",
    ".gq",
    ".cf",
    ".ml"
]

# Fake famous brands
fake_brands = [
    "g00gle",
    "gooogle",
    "paypa1",
    "faceb00k",
    "instagrarn",
    "micr0soft",
    "amaz0n",
    "y0utube",
    "gmai1",
    "0penai"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url'].strip().lower()

    # Auto add https
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    # Remove www.
    if domain.startswith("www."):
        domain = domain.replace("www.", "")

    # URL validation regex
    regex = re.compile(
        r'^(https?:\/\/)'
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
        r'(\/.*)?$'
    )

    phishing_score = 0

    # INVALID URL
    if not regex.match(url):

        result = "Invalid URL ⚠️"
        color = "orange"

    # FAKE BRAND PHISHING
    elif any(fake in domain for fake in fake_brands):

        result = "Fake Brand Phishing ❌"
        color = "red"

    # BLOCK .LOCAL DOMAINS
    elif domain.endswith(".local"):

        result = "Fake Local Domain ❌"
        color = "red"

    # SAFE TRUSTED DOMAINS
    elif domain in trusted_domains:

        result = "Safe Website ✅"
        color = "green"

    else:

        # Long URL
        if len(url) > 75:
            phishing_score += 1

        # Too many hyphens
        if url.count("-") >= 2:
            phishing_score += 2

        # @ symbol
        if "@" in url:
            phishing_score += 3

        # IP address check
        ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        if ip_pattern.search(url):
            phishing_score += 3

        # Dangerous domain extensions
        for ext in dangerous_extensions:
            if domain.endswith(ext):
                phishing_score += 3

        # Suspicious keywords
        for word in suspicious_keywords:
            if word in url:
                phishing_score += 1

        # Too many dots
        if url.count(".") > 3:
            phishing_score += 1

        # HTTP only
        if url.startswith("http://"):
            phishing_score += 1

        # Numbers in domain
        if re.search(r'\d', domain):
            phishing_score += 1

        # Random weird domains
        weird_pattern = re.compile(r'[a-z0-9]{20,}')
        if weird_pattern.search(domain):
            phishing_score += 2

        # FINAL RESULT
        if phishing_score >= 5:

            result = "Phishing Website ❌"
            color = "red"

        elif phishing_score >= 3:

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
