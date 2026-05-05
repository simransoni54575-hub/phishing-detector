from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    if "https" in url:
        result = "Safe Website ✅"
        color = "green"
    else:
        result = "Phishing Website ⚠️"
        color = "red"

    return render_template('index.html', result=result, color=color)

if __name__ == "__main__":
    app.run()
