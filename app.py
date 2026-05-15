from flask import Flask, render_template, request
from urllib.parse import urlparse
import difflib
import re

app = Flask(__name__)

# Trusted websites
trusted_domains = [
    "google.com",
    "youtube.com",
    "github.com",
    "facebook.com",
    "instagram.com",
    "amazon.com",
    "microsoft.com",
    "apple.com",
    "linkedin.com",
    "openai.com",
    "netflix.com",
    "paypal.com"
]

# Suspicious keywords
suspicious_keywords = [
    "login",
    "verify",
    "secure",
    "bank",
    "bonus",
    "free",
    "gift",
    "claim",
    "wallet",
    "crypto",
    "signin",
    "account",
    "update",
    "password"
]

# Dangerous domain extensions
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

        # Auto add https
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        parsed = urlparse(url)

        domain = parsed.netloc.replace("www.", "")

        score = 0

        # =========================
        # INVALID URL CHECK
        # =========================
        regex = re.compile(
            r'^(https?:\/\/)'
            r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
        )

        if not regex.match(url):

            return render_template(
                'index.html',
                result="Invalid URL ⚠️",
                color="orange"
            )

        # =========================
        # LOCAL DOMAIN CHECK
        # =========================
        if ".local" in domain:

            return render_template(
                'index.html',
                result="Fake Local Website ❌",
                color="red"
            )

        # =========================
        # EXACT TRUSTED DOMAIN
        # =========================
        if domain in trusted_domains:

            return render_template(
                'index.html',
                result="Safe Website ✅",
                color="green"
            )

        # =========================
        # TYPO / CLONE DETECTION
        # =========================
        for trusted in trusted_domains:

            similarity = difflib.SequenceMatcher(
                None,
                domain,
                trusted
            ).ratio()

            # Detect:
            # googlle.com
            # g00gle.com
            # gooogle.com

            if similarity > 0.80:

                return render_template(
                    'index.html',
                    result="Fake Copy Website ❌",
                    color="red"
                )

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
        # TOO MANY DASHES
        # =========================
        if domain.count("-") >= 2:
            score += 2

        # =========================
        # TOO MANY DOTS
        # =========================
        if domain.count(".") > 3:
            score += 1

        # =========================
        # @ SYMBOL
        # =========================
        if "@" in url:
            score += 3

        # =========================
        # LONG URL
        # =========================
        if len(url) > 80:
            score += 1

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
        # FINAL RESULT
        # =========================
        if score >= 5:

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
