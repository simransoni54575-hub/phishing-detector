from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)

# 🔍 URL validation
def is_valid_url(url):
    regex = re.compile(
        r'^(https?:\/\/)?'           # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
        r'(\/.*)?$'                  # optional path
    )
    return re.match(regex, url)


# 🧠 Phishing detection logic
def check_url(url):
    score = 0

    # 1. HTTPS check
    if not url.startswith("https"):
        score += 1

    # 2. Suspicious symbols
    if "@" in url or "//" in url[8:]:
        score += 1

    # 3. Long URL
    if len(url) > 75:
        score += 1

    # 4. Hyphen in domain
    domain = urlparse(url).netloc
    if "-" in domain:
        score += 1

    # 5. IP address check
    ip_pattern = r"(http[s]?://)?(\d{1,3}\.){3}\d{1,3}"
    if re.match(ip_pattern, url):
        score += 1

    return score


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.form['url'].strip()

        # ❌ Empty input
        if not user_input:
            return render_template('index.html', result="Please enter a URL ⚠️")

        # 🔧 Add http if missing
        if not user_input.startswith("http"):
            user_input = "http://" + user_input

        # ❌ Invalid URL format
        if not is_valid_url(user_input):
            return render_template('index.html', result="Invalid URL ❌")

        # 🧠 Check phishing
        score = check_url(user_input)

        if score >= 2:
            result = "Phishing Website ❌"
        else:
            result = "Safe Website ✅"

        return render_template('index.html', result=result)

    except Exception as e:
        return render_template('index.html', result="Something went wrong ⚠️")


if __name__ == '__main__':
    app.run(debug=True)
