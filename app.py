from flask import Flask, render_template, request
from urllib.parse import urlparse
import difflib
import re

app = Flask(__name__)

# =========================
# TRUSTED DOMAINS
# =========================
trusted_domains = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "github.com",
    "amazon.com",
    "microsoft.com",
    "apple.com",
    "linkedin.com",
    "paypal.com",
    "netflix.com",
    "openai.com",
    "chatgpt.com",
    "whatsapp.com"
]

# =========================
# SHORTENERS
# =========================
shorteners = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "rb.gy"
]

# =========================
# SUSPICIOUS WORDS
# =========================
suspicious_keywords = [
    "login",
    "verify",
    "secure",
    "bank",
    "bonus",
    "gift",
    "claim",
    "free",
    "crypto",
    "wallet",
    "signin",
    "account",
    "password",
    "update",
    "support"
]

# =========================
# DANGEROUS EXTENSIONS
# =========================
dangerous_extensions = [
    ".tk",
    ".xyz",
    ".ru",
    ".top",
    ".cf",
    ".gq",
    ".ml"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    try:

        url = request.form['url'].strip().lower()

        # Auto add HTTPS
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        parsed = urlparse(url)

        domain = parsed.netloc.replace("www.", "")

        score = 0

        # =========================
        # INVALID URL
        # =========================
        regex = re.compile(
            r'^(https?:\/\/)?'
            r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
        )

        if not regex.match(url):

            return render_template(
                'index.html',
                result="Invalid URL ⚠️",
                color="orange"
            )

        # =========================
        # LOCAL DOMAIN
        # =========================
        if ".local" in domain:

            return render_template(
                'index.html',
                result="Fake Local Website ❌",
                color="red"
            )

        # =========================
        # IP ADDRESS URL
        # =========================
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):

            return render_template(
                'index.html',
                result="Phishing IP URL ❌",
                color="red"
            )

        # =========================
        # TRUSTED DOMAIN
        # =========================
        if domain in trusted_domains:

            return render_template(
                'index.html',
                result="Safe Website ✅",
                color="green"
            )

        # =========================
        # TYPO DOMAIN DETECTION
        # =========================
        for trusted in trusted_domains:

            similarity = difflib.SequenceMatcher(
                None,
                domain,
                trusted
            ).ratio()

            # Detect fake copies
            if similarity > 0.75:

                return render_template(
                    'index.html',
                    result="Fake Copy Website ❌",
                    color="red"
                )

        # =========================
        # SHORTENER DETECTION
        # =========================
        for short in shorteners:

            if short in domain:
                score += 3

        # =========================
        # HTTP ONLY
        # =========================
        if url.startswith("http://"):
            score += 2

        # =========================
        # NUMBERS IN DOMAIN
        # =========================
        if re.search(r'\d', domain):
            score += 2

        # =========================
        # MANY HYPHENS
        # =========================
        if domain.count("-") >= 2:
            score += 2

        # =========================
        # MANY DOTS
        # =========================
        if domain.count(".") > 3:
            score += 2

        # =========================
        # @ SYMBOL
        # =========================
        if "@" in url:
            score += 3

        # =========================
        # LONG URL
        # =========================
        if len(url) > 100:
            score += 2

        # =========================
        # SUSPICIOUS WORDS
        # =========================
        for word in suspicious_keywords:

            if word in url:
                score += 1

        # =========================
        # DANGEROUS EXTENSIONS
        # =========================
        for ext in dangerous_extensions:

            if domain.endswith(ext):
                score += 3

        # =========================
        # RANDOM CHARACTERS
        # =========================
        if re.search(r'[0-9]{3,}', domain):
            score += 2

        # =========================
        # FINAL RESULT
        # =========================
        if score >= 6:

            result = "Phishing Website ❌"
            color = "red"

        elif score >= 3:

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

    except Exception as e:

        return render_template(
            'index.html',
            result="Server Error ⚠️",
            color="red"
        )


if __name__ == "__main__":
    app.run(debug=True)
