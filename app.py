from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # demo prediction (fix model input issue)
    prediction = model.predict([url])[0]

    if prediction == 1:
        result = "Phishing Website ❌"
    else:
        result = "Safe Website ✅"

    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run()
