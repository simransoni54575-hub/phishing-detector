from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return "PhishGuard API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    # simple demo (tu apna ML logic laga sakta hai)
    if "https" in url:
        result = "Safe"
    else:
        result = "Phishing"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()