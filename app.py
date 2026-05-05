from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)

# 🧠 Basic phishing detection function
def check_url(url):
    score = 0

    # 1. HTTPS check
    if not url.startswith("https"):
        score += 1

    # 2. Suspicious symbols
    if "@" in url or "//" in url[8:]:
        score += 1

    # 3. URL length check
    if len(url) > 75:
        score += 1

    # 4. Hyphen in domain
    domain = urlparse(url).netloc
    if "-" in domain:
        score += 1

    # 5. IP address instead of domain
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
        url = request.form['url']

        # 🔧 fix: agar http/https nahi hai toh add kar do
        if not url.startswith("http"):
            url = "http://" + url

        score = check_url(url)

        # 🎯 final decision
        if score >= 2:
            result = "Phishing Website ❌"
        else:
            result = "Safe Website ✅"

        return render_template('index.html', result=result)

    except Exception as e:
        return render_template('index.html', result="Error occurred ⚠️")


if __name__ == '__main__':
    app.run(debug=True)
