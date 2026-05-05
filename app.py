from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# model load
model = pickle.load(open("model.pkl", "rb"))

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# PREDICT
@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    
    # yaha tu apna feature extraction logic laga sakta hai
    # abhi demo ke liye simple predict
    prediction = model.predict([url])[0]

    return f"Result: {prediction}"

if __name__ == "__main__":
    app.run()