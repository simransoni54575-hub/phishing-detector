from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)

# model load
model = pickle.load(open("model.pkl", "rb"))

# -------- FEATURE EXTRACTION --------
def extract_features(url):
    features = []

    # length of URL
    features.append(len(url))

    # has https
    features.append(1 if "https" in url else 0)

    # number of dots
    features.append(url.count("."))

    # has @
    features.append(1 if "@" in url else 0)

    # has -
    features.append(1 if "-" in url else 0)

    return features

# HOME
@app.route('/')
def home():
    return render_template("index.html")

# PREDICT
@app.route('/predict', methods=['POST'])
def predict():
    try:
        url = request.form['url']

        features = extract_features(url)
        prediction = model.predict([features])[0]

        if prediction == 1:
            result = "Safe Website ✅"
        else:
            result = "Phishing Website ⚠️"

        return render_template("index.html", result=result)

    except Exception as e:
        return render_template("index.html", result="Error occurred ⚠️")

if __name__ == "__main__":
    app.run(debug=True)
